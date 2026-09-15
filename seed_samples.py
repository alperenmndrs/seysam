"""Insert the user-requested sample logo layout once; never restore deleted records."""
from seysa import storage

SAMPLES = [
    ('ASKON', 'İş dünyası', 'https://www.askon.org.tr/', 'askon.png'),
    ('T.C. Kültür ve Turizm Bakanlığı', 'Kamu', 'https://www.ktb.gov.tr/', 'kultur-turizm.svg'),
    ('T.C. Ulaştırma ve Altyapı Bakanlığı', 'Kamu', 'https://www.uab.gov.tr/', 'ulastirma.png'),
    ('KOSGEB', 'Kamu', 'https://www.kosgeb.gov.tr/', 'kosgeb.png'),
    ('Kıyı Emniyeti Genel Müdürlüğü', 'Kamu', 'https://www.kiyiemniyeti.gov.tr/', 'kiyi-emniyeti.png'),
]

def seed():
    storage.initialize()
    with storage.connect() as db:
        if db.execute("SELECT 1 FROM app_meta WHERE key='sample_logos_v1'").fetchone():
            print('Örnek logolar daha önce eklenmiş; mevcut kayıtlar korunuyor.')
            return
        for index,(name,sector,website,file) in enumerate(SAMPLES):
            if not (storage.ROOT/'assets'/'references'/file).is_file(): raise RuntimeError('Missing logo: '+file)
            company=db.execute('INSERT INTO companies(name,sector,website,logo) VALUES(?,?,?,?)',(name,sector,website,'/assets/references/'+file)).lastrowid
            db.execute('INSERT INTO reference_items(company_id,is_sample,published,position) VALUES(?,1,1,?)',(company,index))
        db.execute("INSERT INTO app_meta(key,value) VALUES('sample_logos_v1','1')")
    print('Beş örnek logo eklendi. Yönetici hesabı ilk açılışta oluşturulacak.')

if __name__=='__main__':seed()
