import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://wequqsbvhydvugifevhm.supabase.co";
const supabaseAnonKey = "sb_publishable_ZOfGu0PLriJqtJLdmk6Bkg_mJ3HrURB";

export const supabase = createClient(supabaseUrl, supabaseAnonKey);