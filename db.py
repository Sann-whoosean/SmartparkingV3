from supabase import create_client, Client
import os

SUPABASE_URL = os.environ.get("https://foxynxknymenhcaonxrl.supabase.co")
SUPABASE_KEY = os.environ.get("sb_publishable_0VDWVK7C-VSPHp9539BG5Q_YhYnyS0O")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_db():
    return supabase