from django.db import migrations, models
from django.contrib.postgres.fields import JSONField

def partition_localize_accommodation(apps, schema_editor):
    """
    Custom migration function to partition the LocalizeAccommodation table by language
    """
    # Use the schema editor's connection
    connection = schema_editor.connection
    cursor = connection.cursor()

    try:
        # Create the partitioned table WITHOUT foreign key constraint
        cursor.execute("""
        CREATE TABLE app_localizeaccommodation_partitioned (
            id SERIAL,
            property_id VARCHAR(100) NOT NULL,
            language VARCHAR(2) NOT NULL,
            description TEXT NOT NULL,
            policy JSONB DEFAULT '{}',
            PRIMARY KEY (id, language)
        ) PARTITION BY LIST (language);
        """)

        # Create partitions for common languages
        languages = ['en', 'es', 'fr', 'de', 'it', 'zh', 'ja', 'ko', 'ru', 'ar']
        for lang in languages:
            cursor.execute(f"""
            CREATE TABLE app_localizeaccommodation_partition_{lang} 
            PARTITION OF app_localizeaccommodation_partitioned 
            FOR VALUES IN ('{lang}');
            """)

        # Create a default partition for any other languages
        cursor.execute("""
        CREATE TABLE app_localizeaccommodation_partition_other 
        PARTITION OF app_localizeaccommodation_partitioned 
        DEFAULT;
        """)

        # Copy existing data to the new partitioned table
        cursor.execute("""
        INSERT INTO app_localizeaccommodation_partitioned 
        (id, property_id, language, description, policy)
        SELECT id, property_id, language, description, policy 
        FROM app_localizeaccommodation;
        """)

        # Drop the original table
        cursor.execute("DROP TABLE app_localizeaccommodation;")

        # Rename the partitioned table to the original table name
        cursor.execute("""
        ALTER TABLE app_localizeaccommodation_partitioned 
        RENAME TO app_localizeaccommodation;
        """)

    except Exception as e:
        # Print the full error for debugging
        print(f"Migration error: {e}")
        raise e
    finally:
        cursor.close()

def reverse_partition_localize_accommodation(apps, schema_editor):
    """
    Reverse migration to revert partitioning
    """
    connection = schema_editor.connection
    cursor = connection.cursor()

    try:
        # Recreate the original non-partitioned table
        cursor.execute("""
        CREATE TABLE app_localizeaccommodation (
            id SERIAL PRIMARY KEY,
            property_id VARCHAR(100) NOT NULL,
            language VARCHAR(2) NOT NULL,
            description TEXT NOT NULL,
            policy JSONB DEFAULT '{}'
        );
        """)

        # Copy data from the partitioned table
        cursor.execute("""
        INSERT INTO app_localizeaccommodation 
        (id, property_id, language, description, policy)
        SELECT id, property_id, language, description, policy 
        FROM app_localizeaccommodation;
        """)

        # Drop the partitioned table and its partitions
        cursor.execute("DROP TABLE app_localizeaccommodation CASCADE;")

    except Exception as e:
        print(f"Reverse migration error: {e}")
        raise e
    finally:
        cursor.close()

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0002_partition_accommodation'),  # Previous migration file
    ]

    operations = [
        migrations.RunPython(
            partition_localize_accommodation, 
            reverse_partition_localize_accommodation
        )
    ]