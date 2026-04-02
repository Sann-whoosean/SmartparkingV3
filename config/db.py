import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


def get_db():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    print(f"DEBUG: URL={url}, KEY={key}")
    if not url or not key:
        
        print(f"DEBUG: URL={url}, KEY={key}")
        raise ValueError("SUPABASE_URL atau SUPABASE_KEY tidak ditemukan di .env")

    try:

        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        print(f"❌ Gagal inisialisasi Supabase: {e}")
        return None


supabase_client = get_db()
