# Generated by Django 4.1.6 on 2023-02-11 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bhpwoo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['last_name']},
        ),
        migrations.AlterModelOptions(
            name='position',
            options={},
        ),
        migrations.AlterModelOptions(
            name='protectiveclothing',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='protectiveclothingrelease',
            options={'ordering': ['release_date']},
        ),
        migrations.AlterModelOptions(
            name='protectiveclothingset',
            options={'ordering': ['name']},
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='firstname',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='lastname',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='protectiveclothingrelease',
            old_name='set',
            new_name='pc_set',
        ),
        migrations.RenameField(
            model_name='protectiveclothingrelease',
            old_name='when',
            new_name='release_date',
        ),
        migrations.RenameField(
            model_name='protectiveclothingset',
            old_name='set',
            new_name='pc_set',
        ),
        migrations.AddField(
            model_name='employee',
            name='obtained_set',
            field=models.PositiveIntegerField(null=True, verbose_name='Otrzymany zestaw'),
        ),
        migrations.AddField(
            model_name='protectiveclothing',
            name='price',
            field=models.PositiveIntegerField(null=True, verbose_name='Cena odzieży'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bhpwoo.position', verbose_name='Stanowisko pracownika'),
        ),
        migrations.AlterField(
            model_name='position',
            name='position_type',
            field=models.CharField(choices=[('Kadra zarządzająca', (('DP', 'Dyrektor pionu'), ('KR', 'Kierownik'), ('LZ', 'Lider zespołu'))), ('Specjaliści i pracownicy wsparcia', (('EK', 'Ekspert'), ('SS', 'Starszy specjalista'), ('MS', 'Młodszy specjalista'))), ('Pracownicy fizyczni', (('BR', 'Brygadzista'), ('PC', 'Programista CNC'), ('FC', 'Frezer CNC'), ('TC', 'Tokarz CNC'), ('MT', 'Monter'), ('TK', 'Tokarz'), ('SL', 'Ślusarz'), ('FR', 'Frezer'), ('SZ', 'Szlifierz'), ('SP', 'Spawacz'), ('LK', 'Lakiernik'), ('BL', 'Blacharz'), ('OW', 'Operator wózka'), ('EL', 'Elektryk'), ('ET', 'Elektryk ds. wysokich napięć')))], default=1, max_length=2, unique=True, verbose_name='Stanowisko'),
        ),
    ]