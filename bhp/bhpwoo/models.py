from django.db import models
from django.utils.html import format_html
from django.db.models.signals import post_save


SEX_CHOICES = [
    ('M', 'Mężczyzna'),
    ('F', 'Kobieta'),
]


POSITION_CHOICES = [
    ('Kadra zarządzająca', (
        ('DP', 'Dyrektor pionu'),
        ('KR', 'Kierownik'),
        ('LZ', 'Lider zespołu'),
    )),
    ('Specjaliści i pracownicy wsparcia', (
        ('EK', 'Ekspert'),
        ('SS', 'Starszy specjalista'),
        ('MS', 'Młodszy specjalista'),
    )),
    ('Pracownicy fizyczni', (
        ('BR', 'Brygadzista'),
        ('PC', 'Programista CNC'),
        ('FC', 'Frezer CNC'),
        ('TC', 'Tokarz CNC'),
        ('MT', 'Monter'),
        ('TK', 'Tokarz'),
        ('SL', 'Ślusarz'),
        ('FR', 'Frezer'),
        ('SZ', 'Szlifierz'),
        ('SP', 'Spawacz'),
        ('LK', 'Lakiernik'),
        ('BL', 'Blacharz'),
        ('OW', 'Operator wózka'),
        ('EL', 'Elektryk'),
        ('ET', 'Elektryk ds. wysokich napięć'),
    )),
]


class Position(models.Model):
    """
    Job Position. It serves as a basis in the selection of a specific set of protective clothing for the company's employees.
    """
    position_type = models.CharField(max_length=2, choices=POSITION_CHOICES, default=1, verbose_name="Stanowisko", unique=True)

    def __str__(self):
        return f"{self.get_position_type_display()}"


class Employee(models.Model):
    """
    The model stores basic employee data. In addition to personal data and position, in the database is stored
    information about what BHP kit the employee has received (initially the value of this field is null)
    """
    first_name = models.CharField(max_length=25, verbose_name="Imię")
    last_name = models.CharField(max_length=40, verbose_name="Nazwisko")
    age = models.PositiveIntegerField(verbose_name="Wiek")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default="M", verbose_name="Płeć")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Stanowisko pracownika")
    obtained_set = models.PositiveIntegerField(verbose_name="Otrzymany zestaw", null=True)

    class Meta:
        ordering = ['last_name']
        db_table = "employees"

    def __str__(self):
        return f"{self.first_name} {self.last_name} (na stanowisku: {self.position}, {self.age} lat)"


class ProtectiveClothing(models.Model):
    """
    Model stores information about protective clothing - that is, the individual components needed to assemble kits.
    Model saves name, link to a photo and price of protective clothing in database.
    """
    name = models.CharField(max_length=50, verbose_name="Nazwa odzieży")
    image = models.ImageField(upload_to='images/', verbose_name="Zdjęcie odzieży", null=True)
    price = models.PositiveIntegerField(verbose_name="Cena odzieży", null=True)

    def image_tag(self):
        return format_html('<img href="{0}" src="{0}" width="100" height="100" />'.format(self.image.url))

    image_tag.allow_tags = True
    image_tag.short_description = 'Image'

    class Meta:
        ordering = ['name']
        db_table = "protective_clothes"

    def __str__(self):
        return f"Odzież ochronna: {self.name}"


class ProtectiveClothingSet(models.Model):
    """
    Protective clothing sets consisting of selected items, suitable for workers in a particular position. In this
    model, the value (total price of all components) of the set and the number of elements of the set are calculated.
    """

    name = models.CharField(max_length=50, null=True, verbose_name="Skrócona nazwa zestawu odzieży BHP")
    position = models.OneToOneField(Position, on_delete=models.CASCADE, verbose_name="Stanowisko pracownika", null=True)
    pc_set = models.ManyToManyField(ProtectiveClothing,  verbose_name="Wybrane elementy zestawu")

    class Meta:
        ordering = ['name']
        db_table = "protective_clothes_sets"

    def __str__(self):
        return f"{self.name} - zestaw odzieży ochronnej dla pracownika na stanowisku: {self.position}"

    @property
    def price_of_set(self):
        return sum([p.price for p in self.pc_set.all()])

    @property
    def size_of_set(self):
        return (self.pc_set.all()).count()


class ProtectiveClothingRelease(models.Model):
    """
    The model stores information about the issued sets of protective clothing to the company's employees (their
    issuance is possible from the administration panel, as well as with the help of the corresponding form).
    """

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, verbose_name="Pracownik otrzymujący odzież BHP")
    pc_set = models.ForeignKey(ProtectiveClothingSet, on_delete=models.CASCADE, verbose_name="Wydawany zestaw")
    release_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['release_date']
        db_table = "protective_clothes_release"

    def __str__(self):
        return f"Wydano ({self.release_date}) zestaw odzieży ochronnej dla pracownika: {self.employee}"

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        e = Employee.objects.get(id=instance.employee.id)
        e.obtained_set = instance.pc_set.id
        e.save()


post_save.connect(ProtectiveClothingRelease.post_create, sender=ProtectiveClothingRelease)