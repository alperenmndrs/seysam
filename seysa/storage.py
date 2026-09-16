"""SQLite persistence and local media. The private data directory is never served."""
import hashlib
import os
import secrets
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(os.environ.get('SEYSA_DATA_DIR', str(ROOT / '.data'))).resolve()
DB = DATA / 'seysa.sqlite3'
UPLOADS = DATA / 'uploads'

def connect():
    db = sqlite3.connect(DB, timeout=15)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db

def initialize():
    DATA.mkdir(parents=True, exist_ok=True, mode=0o700)
    UPLOADS.mkdir(exist_ok=True, mode=0o700)
    with connect() as db:
        db.execute('PRAGMA journal_mode = WAL')
        db.executescript('''
        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY CHECK(id=1), username TEXT NOT NULL UNIQUE, password TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS sessions (token TEXT PRIMARY KEY, csrf TEXT NOT NULL, user_id INTEGER REFERENCES users(id), expires INTEGER NOT NULL);
        CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires);
        CREATE TABLE IF NOT EXISTS login_attempts (ip TEXT PRIMARY KEY, failures INTEGER NOT NULL DEFAULT 0, blocked_until INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS companies (id INTEGER PRIMARY KEY, name TEXT NOT NULL, sector TEXT NOT NULL DEFAULT '', website TEXT NOT NULL DEFAULT '', logo TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, company_id INTEGER REFERENCES companies(id) ON DELETE SET NULL, title TEXT NOT NULL, summary TEXT NOT NULL DEFAULT '', body TEXT NOT NULL DEFAULT '', service TEXT NOT NULL DEFAULT '', image TEXT NOT NULL DEFAULT '', published INTEGER NOT NULL DEFAULT 0 CHECK(published IN (0,1)), position INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
        CREATE INDEX IF NOT EXISTS idx_projects_published_position ON projects(published,position);
        CREATE TABLE IF NOT EXISTS project_media (id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE, kind TEXT NOT NULL CHECK(kind IN ('image','video')), url TEXT NOT NULL, caption TEXT NOT NULL DEFAULT '', position INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS reference_items (id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL UNIQUE REFERENCES companies(id) ON DELETE CASCADE, quote TEXT NOT NULL DEFAULT '', author TEXT NOT NULL DEFAULT '', is_sample INTEGER NOT NULL DEFAULT 0 CHECK(is_sample IN (0,1)), published INTEGER NOT NULL DEFAULT 0 CHECK(published IN (0,1)), position INTEGER NOT NULL DEFAULT 0);
        CREATE INDEX IF NOT EXISTS idx_references_published_position ON reference_items(published,position);
        CREATE TABLE IF NOT EXISTS app_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        ''')
        db.execute('PRAGMA optimize')
        columns={row['name'] for row in db.execute('PRAGMA table_info(projects)')}
        for name in ('brief','process','result'):
            if name not in columns: db.execute('ALTER TABLE projects ADD COLUMN '+name+" TEXT NOT NULL DEFAULT ''")
        for key,value in {'whatsapp':'905888888888', 'address':'Prestige 24 Plaza N:10 Bahçelievler/İstanbul', 'instagram':'https://www.instagram.com/seysamedya/', 'linkedin':'https://www.linkedin.com/company/seysamedya/'}.items():
            db.execute('INSERT OR IGNORE INTO app_meta(key,value) VALUES(?,?)',('site_'+key,value))
    if DB.exists(): os.chmod(DB, 0o600)

def password_hash(password):
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 600000).hex()
    return 'pbkdf2_sha256$600000$' + salt + '$' + digest

def password_matches(password, stored):
    try:
        algo, count, salt, digest = stored.split('$')
        if algo != 'pbkdf2_sha256': return False
        actual = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), int(count)).hex()
        return secrets.compare_digest(actual, digest)
    except (ValueError, TypeError):
        return False

def public_data():
    with connect() as db:
        projects = [dict(r) for r in db.execute('SELECT p.*, c.name AS company_name FROM projects p LEFT JOIN companies c ON c.id=p.company_id WHERE p.published=1 ORDER BY p.position, p.id DESC')]
        refs = [dict(r) for r in db.execute('SELECT r.*, c.name, c.logo, c.sector, c.website FROM reference_items r JOIN companies c ON c.id=r.company_id WHERE r.published=1 ORDER BY r.position, r.id')]
        media = [dict(r) for r in db.execute('SELECT m.* FROM project_media m JOIN projects p ON p.id=m.project_id WHERE p.published=1 ORDER BY m.position,m.id')]
        for project in projects: project['gallery'] = [m for m in media if m['project_id']==project['id']]
    return projects, refs

def site_settings():
    with connect() as db:
        return {r['key'][5:]:r['value'] for r in db.execute("SELECT key,value FROM app_meta WHERE key IN ('site_whatsapp','site_address','site_instagram','site_linkedin')")}
