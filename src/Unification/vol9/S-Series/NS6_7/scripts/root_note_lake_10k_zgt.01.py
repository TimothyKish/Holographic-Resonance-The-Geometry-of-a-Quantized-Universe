from astroquery.vizier import Vizier

# Set the 9,999 limit and all columns
v = Vizier(columns=['*', 'Vdisp', 'zsp', 'rpmag'], row_limit=9999)

# The Mondy Cut: z < 0.1, velDisp > 100, and must be a Galaxy
query = "V/154/sdss16"
constraints = {"class": "==3", "zsp": "<0.1", "Vdisp": ">100"}

print("🛰️ Connecting to the Backbone...")
result = v.query_constraints(catalog=query, **constraints)

if result:
    df = result[0].to_pandas()
    df.to_csv('../lake/root_note_lake.csv', index=False)
    print(f"✅ Lake Filled: {len(df)} clean probes saved to root_note_lake.csv")
else:
    print("❌ Even the backbone is silent. The storm is heavy.")