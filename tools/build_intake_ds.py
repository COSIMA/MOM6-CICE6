from access_nri_intake.source import builders

builder = builders.AccessOm3Builder(
    path='archive/'
)

builder.build()

# Log invalid assets:

builder.invalid_assets

# Save the datastore to a file (json)

builder.save(name='intake_datastore', description='How do I get this from metadata.yaml', directory='archive/')