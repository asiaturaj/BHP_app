from django.db import models
from django.utils.html import format_html


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
        ('OC', 'Operator CNC'),
        ('PC', 'Programista CNC'),
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
    Model dla stanowiska pracy
    """
    position_type = models.CharField(max_length=2, choices=POSITION_CHOICES, default=1, verbose_name="Stanowisko", unique=True)

    class Meta:
        verbose_name_plural = "1. Stanowiska"

    def __str__(self):
        return f"{self.get_position_type_display()}"


class Employee(models.Model):
    # """
    # Model z danymi pracownika
    # """
    firstname = models.CharField(max_length=25, verbose_name="Imię")
    lastname = models.CharField(max_length=40, verbose_name="Nazwisko")
    age = models.PositiveIntegerField(verbose_name="Wiek")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default="M", verbose_name="Płeć")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Stanowisko pracownika", null=True)

    class Meta:
        ordering = ['lastname']
        db_table = "employees"
        verbose_name_plural = "2. Pracownicy"

    def __str__(self):
        return f"{self.firstname} {self.lastname} (na stanowisku: {self.position}, {self.age} lat)"


class ProtectiveClothing(models.Model):
    """
    Model Odzieży ochronnej- pojedyncze środki ochrony potrzebne do złożenia zestawu
    """
    name = models.CharField(max_length=50, verbose_name="Nazwa odzieży")
    image = models.ImageField(upload_to='images/', verbose_name="Zdjęcie odzieży", null=True)

    def image_tag(self):
        return format_html('<img href="{0}" src="{0}" width="100" height="100" />'.format(self.image.url))

    image_tag.allow_tags = True
    image_tag.short_description = 'Image'

    class Meta:
        ordering = ['name']
        db_table = "protective_clothes"
        verbose_name_plural = "3. Odzież ochronna"

    def __str__(self):
        return f"Odzież ochronna: {self.name}"


class ProtectiveClothingSet(models.Model):
    """
    Zestawy odzieży ochronnej składające się z wybranych elementów, odpowiednie dla pracowników na danym stanowisku
    """

    name = models.CharField(max_length=50, null=True, verbose_name="Skrócona nazwa zestawu odzieży BHP")
    position = models.OneToOneField(Position, on_delete=models.CASCADE, verbose_name="Stanowisko pracownika", null=True)
    set = models.ManyToManyField(ProtectiveClothing,  verbose_name="Wybrane elementy zestawu")

    class Meta:
        ordering = ['name']
        db_table = "protective_clothes_sets"
        verbose_name_plural = "4. Zestawy odzieży ochronnej"

    def __str__(self):
        return f"{self.name} - zestaw odzieży ochronnej dla pracownika na stanowisku: {self.position}"


class ProtectiveClothingRelease(models.Model):
    """
    Wydanie zestawu odzieży ochronnej pracownikowi
    """

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, verbose_name="Pracownik otrzymujący odzież BHP")
    set = models.ForeignKey(ProtectiveClothingSet, on_delete=models.CASCADE, verbose_name="Wydawany zestaw")
    when = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['when']
        db_table = "protective_clothes_release"
        verbose_name_plural = "5. Wydanie zestawów odzieży ochronnej"

    def __str__(self):
        return f"Wydano ({self.when}) zestaw odzieży ochronnej dla pracownika: {self.employee}"
