from django.db import migrations, models
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError

class Migration(migrations.Migration):
    dependencies = [
        # Replace with the actual last migration of your app
        ('app', '0001_initial'),
    ]

    def partition_accommodation_table(apps, schema_editor):
        """
        Partition the Accommodation table based on feed ranges
        """
        # Get the connection to use PostgreSQL-specific operations
        from django.db import connections
        db_alias = schema_editor.connection.alias

        # SQL to create partitioned table with composite primary key
        create_partitioned_table = """
        CREATE TABLE new_app_accommodation (
            id VARCHAR(20) NOT NULL,
            feed SMALLINT NOT NULL,
            title VARCHAR(100) NOT NULL,
            country_code VARCHAR(2) NOT NULL,
            bedroom_count INTEGER NOT NULL,
            review_score DECIMAL(3, 1) NOT NULL DEFAULT 0,
            usd_rate DECIMAL(10, 2) NOT NULL,
            center geometry(Point, 4326) NOT NULL,  
            images TEXT[],
            location_id VARCHAR(20) NOT NULL,
            amenities JSONB,
            user_id INTEGER NOT NULL,  -- Changed to INTEGER to match auth_user.id type
            published BOOLEAN NOT NULL DEFAULT false,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL,

            PRIMARY KEY (feed, id),

            FOREIGN KEY (location_id) REFERENCES app_location (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES auth_user (id) ON DELETE CASCADE
        ) PARTITION BY RANGE (feed);

        -- Create partitions for different feed ranges
        CREATE TABLE accommodation_feed_0_500 
        PARTITION OF new_app_accommodation 
        FOR VALUES FROM (0) TO (501);

        CREATE TABLE accommodation_feed_501_2000 
        PARTITION OF new_app_accommodation 
        FOR VALUES FROM (501) TO (2001);

        CREATE TABLE accommodation_feed_2001_5000 
        PARTITION OF new_app_accommodation 
        FOR VALUES FROM (2001) TO (5001);

        CREATE TABLE accommodation_feed_5000_plus 
        PARTITION OF new_app_accommodation 
        FOR VALUES FROM (5001) TO (MAXVALUE);
        """

        # SQL to copy existing data to the new partitioned table
        copy_data = """
        INSERT INTO new_app_accommodation (id, feed, title, country_code, bedroom_count, review_score, usd_rate, center, images, location_id, amenities, user_id, published, created_at, updated_at)
        SELECT id, feed, title, country_code, bedroom_count, review_score, usd_rate, 
               ST_SetSRID(center, 4326) AS center,  -- Ensure the geometry has the correct SRID
               images, location_id, amenities, user_id, published, created_at, updated_at
        FROM app_accommodation;
        """

        # SQL to drop the old table and rename the new one (use CASCADE)
        finalize_migration = """
        -- Drop foreign key constraints that reference app_accommodation before dropping it
        ALTER TABLE app_localizeaccommodation DROP CONSTRAINT IF EXISTS app_localizeaccommod_property_id_e9fbb0ea_fk_app_accom;

        -- Drop the old table and rename the new partitioned table
        DROP TABLE app_accommodation CASCADE;
        ALTER TABLE new_app_accommodation RENAME TO app_accommodation;
        """

        # Execute the migration steps
        with connections[db_alias].cursor() as cursor:
            cursor.execute(create_partitioned_table)
            cursor.execute(copy_data)
            cursor.execute(finalize_migration)

    def reverse_migration(apps, schema_editor):
        """
        Reverse the partitioning if needed
        """
        # Get the connection to use PostgreSQL-specific operations
        from django.db import connections
        db_alias = schema_editor.connection.alias

        # SQL to convert back to a regular table
        revert_partitioning = """
        CREATE TABLE new_app_accommodation AS 
        SELECT * FROM app_accommodation;

        DROP TABLE app_accommodation;
        ALTER TABLE new_app_accommodation RENAME TO app_accommodation;
        """

        with connections[db_alias].cursor() as cursor:
            cursor.execute(revert_partitioning)

    operations = [
        migrations.RunPython(partition_accommodation_table, reverse_migration),
    ]
