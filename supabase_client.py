from supabase import create_client

SUPABASE_URL = "https://wequqsbvhydvugifevhm.supabase.co"
SUPABASE_KEY = "sb_publishable_ZOfGu0PLriJqtJLdmk6Bkg_mJ3HrURB"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)