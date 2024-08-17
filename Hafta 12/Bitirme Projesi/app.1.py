from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

class KarbonAyakIziHesaplayici:
    def __init__(self, veri):
        self.veri = veri

    def elektrik_emisyonu_hesapla(self):
        try:
            kisi_sayisi = int(self.veri.get('kisi_sayisi', 0))
            elektrik_faturasi = float(self.veri.get('elektrik_faturasi', 0))
            emisyon_faktoru = 0.5
            kWh = elektrik_faturasi / 0.10
            return kWh * emisyon_faktoru
        except (ValueError, TypeError) as e:
            raise ValueError("Elektrik emisyonu hesaplaması için geçersiz giriş.") from e

    def dogal_gaz_emisyonu_hesapla(self):
        try:
            ocak = float(self.veri.get('ocak', 0))
            nisan = float(self.veri.get('nisan', 0))
            temmuz = float(self.veri.get('temmuz', 0))
            ekim = float(self.veri.get('ekim', 0))
            emisyon_faktoru = 2.2
            ortalama_aylik_tuketim = (ocak + nisan + temmuz + ekim) / 4
            return ortalama_aylik_tuketim * 12 * emisyon_faktoru
        except (ValueError, TypeError) as e:
            raise ValueError("Doğal gaz emisyonu hesaplaması için geçersiz giriş.") from e

    def yakit_emisyonu_hesapla(self):
        try:
            yillik_yakit = float(self.veri.get('yillik_yakit', 0))
            emisyon_faktoru = 2.5
            return yillik_yakit * emisyon_faktoru
        except (ValueError, TypeError) as e:
            raise ValueError("Yakıt emisyonu hesaplaması için geçersiz giriş.") from e

    def arac_emisyonu_hesapla(self):
        try:
            arac_var_mi = self.veri.get('arac_var_mi') == 'evet'
            if not arac_var_mi:
                return 0
            motor_tipi = self.veri.get('arac_motor_tipi')
            yillik_mesafe = float(self.veri.get('arac_yillik_mesafe', 0))
            emisyon_faktoru = 2.3 if motor_tipi == 'benzinli' else 2.7
            yakit_verimliligi = 10
            tuketilen_litre = yillik_mesafe / yakit_verimliligi
            return tuketilen_litre * emisyon_faktoru
        except (ValueError, TypeError) as e:
            raise ValueError("Araç emisyonu hesaplaması için geçersiz giriş.") from e

    def motosiklet_emisyonu_hesapla(self):
        try:
            motosiklet_var_mi = self.veri.get('motosiklet_var_mi') == 'evet'
            if not motosiklet_var_mi:
                return 0
            motor_tipi = self.veri.get('motosiklet_motor_tipi')
            yillik_mesafe = float(self.veri.get('motosiklet_yillik_mesafe', 0))
            emisyon_faktoru = 2.3 if motor_tipi == 'benzinli' else 2.7
            yakit_verimliligi = 20
            tuketilen_litre = yillik_mesafe / yakit_verimliligi
            return tuketilen_litre * emisyon_faktoru
        except (ValueError, TypeError) as e:
            raise ValueError("Motosiklet emisyonu hesaplaması için geçersiz giriş.") from e

    def seyahat_emisyonu_hesapla(self):
        try:
            seyahat_sayilari = {
                "Turkiye/Avrupa": int(self.veri.get('turkiye_avrupa', 0)),
                "Avrupa/Amerika": int(self.veri.get('avrupa_amerika', 0)),
                "Turkiye/Amerika": int(self.veri.get('turkiye_amerika', 0)),
                "Turkiye/Uzakdogu": int(self.veri.get('turkiye_uzakdogu', 0))
            }
            emisyon_faktorlari = {
                "Turkiye/Avrupa": 0.2,
                "Avrupa/Amerika": 0.5,
                "Turkiye/Amerika": 1.0,
                "Turkiye/Uzakdogu": 1.5
            }
            mesafeler = {
                "Turkiye/Avrupa": 2500,
                "Avrupa/Amerika": 7000,
                "Turkiye/Amerika": 9000,
                "Turkiye/Uzakdogu": 8000
            }
            toplam_emisyon = 0
            for kategori, sayi in seyahat_sayilari.items():
                toplam_emisyon += sayi * mesafeler[kategori] * emisyon_faktorlari[kategori]
            return toplam_emisyon
        except (ValueError, TypeError) as e:
            raise ValueError("Seyahat emisyonu hesaplaması için geçersiz giriş.") from e

    def toplam_emisyon_hesapla(self):
        try:
            elektrik_emisyonu = self.elektrik_emisyonu_hesapla()
            dogal_gaz_emisyonu = self.dogal_gaz_emisyonu_hesapla()
            yakit_emisyonu = self.yakit_emisyonu_hesapla()
            arac_emisyonu = self.arac_emisyonu_hesapla()
            motosiklet_emisyonu = self.motosiklet_emisyonu_hesapla()
            seyahat_emisyonu = self.seyahat_emisyonu_hesapla()

            toplam_emisyon = (elektrik_emisyonu + dogal_gaz_emisyonu + yakit_emisyonu +
                              arac_emisyonu + motosiklet_emisyonu + seyahat_emisyonu)
            
            return {
                'toplam_emisyon': toplam_emisyon,
                'elektrik_emisyonu': elektrik_emisyonu,
                'dogal_gaz_emisyonu': dogal_gaz_emisyonu,
                'yakit_emisyonu': yakit_emisyonu,
                'arac_emisyonu': arac_emisyonu,
                'motosiklet_emisyonu': motosiklet_emisyonu,
                'seyahat_emisyonu': seyahat_emisyonu,
                'agac_sayisi': self.agac_sayisi_hesapla(toplam_emisyon)
            }
        except ValueError as e:
            raise
    
    def agac_sayisi_hesapla(self, toplam_emisyon):
        return int(toplam_emisyon / 6700)

@app.route('/', methods=['GET', 'POST'])
def ana_sayfa():
    if request.method == 'POST':
        try:
            hesaplayici = KarbonAyakIziHesaplayici(request.form)
            sonuclar = hesaplayici.toplam_emisyon_hesapla()

            sonuc_html = '''
            <!DOCTYPE html>
            <html lang="tr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Karbon Ayak İzi Sonucu</title>
                <style>
                    body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }
                    .container { max-width: 600px; margin: 50px auto; background-color: #fff; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
                    h1 { text-align: center; color: #333; }
                    ul { list-style-type: none; padding: 0; }
                    li { margin: 10px 0; color: #333; }
                    a { display: block; text-align: center; margin-top: 20px; color: #5cb85c; text-decoration: none; }
                    a:hover { color: #4cae4c; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Karbon Ayak İzi Sonuçları</h1>
                    <ul>
                        <li>Toplam Emisyon: {{ toplam_emisyon }} kg CO2</li>
                        <li>Gerekli Ağaç Sayısı: {{ agac_sayisi }} ağaç</li>
                        <li>Elektrik Emisyonu: {{ elektrik_emisyonu }} kg CO2</li>
                        <li>Doğal Gaz Emisyonu: {{ dogal_gaz_emisyonu }} kg CO2</li>
                        <li>Yakıt Emisyonu: {{ yakit_emisyonu }} kg CO2</li>
                        <li>Araç Emisyonu: {{ arac_emisyonu }} kg CO2</li>
                        <li>Motosiklet Emisyonu: {{ motosiklet_emisyonu }} kg CO2</li>
                        <li>Seyahat Emisyonu: {{ seyahat_emisyonu }} kg CO2</li>
                    </ul>
                    <a href="/">Başka bir hesaplama yap</a>
                </div>
            </body>
            </html>
            '''
            return render_template_string(sonuc_html, **sonuclar)
        except ValueError as e:
            return jsonify({'hata': str(e)}), 400
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Karbon Ayak İzi Hesaplama</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }
            .container { max-width: 600px; margin: 50px auto; background-color: #fff; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
            h1 { text-align: center; color: #333; }
            label { display: block; margin: 10px 0 5px; color: #333; }
            input[type="text"], input[type="number"], select { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; }
            button { width: 100%; padding: 10px; background-color: #5cb85c; color: white; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background-color: #4cae4c; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Karbon Ayak İzi Hesaplama</h1>
            <form method="POST">
                <label for="kisi_sayisi">Evde Yaşayan Kişi Sayısı:</label>
                <input type="number" id="kisi_sayisi" name="kisi_sayisi" required>

                <label for="elektrik_faturasi">Aylık Elektrik Faturası (TL):</label>
                <input type="text" id="elektrik_faturasi" name="elektrik_faturasi" required>

                <label>Mevsimlere Göre Doğalgaz Tüketimi (m³):</label>
                <input type="text" name="ocak" placeholder="Ocak">
                <input type="text" name="nisan" placeholder="Nisan">
                <input type="text" name="temmuz" placeholder="Temmuz">
                <input type="text" name="ekim" placeholder="Ekim">

                <label for="yillik_yakit">Yıllık Yakıt Tüketimi (litre):</label>
                <input type="text" id="yillik_yakit" name="yillik_yakit" required>

                <label for="arac_var_mi">Araç Sahibi misiniz?</label>
                <select id="arac_var_mi" name="arac_var_mi">
                    <option value="evet">Evet</option>
                    <option value="hayir">Hayır</option>
                </select>

                <label for="arac_motor_tipi">Araç Motor Tipi:</label>
                <select id="arac_motor_tipi" name="arac_motor_tipi">
                    <option value="benzinli">Benzinli</option>
                    <option value="dizel">Dizel</option>
                </select>

                <label for="arac_yillik_mesafe">Yıllık Araçla Yapılan Mesafe (km):</label>
                <input type="text" id="arac_yillik_mesafe" name="arac_yillik_mesafe" required>

                <label for="motosiklet_var_mi">Motosiklet Sahibi misiniz?</label>
                <select id="motosiklet_var_mi" name="motosiklet_var_mi">
                    <option value="evet">Evet</option>
                    <option value="hayir">Hayır</option>
                </select>

                <label for="motosiklet_motor_tipi">Motosiklet Motor Tipi:</label>
                <select id="motosiklet_motor_tipi" name="motosiklet_motor_tipi">
                    <option value="benzinli">Benzinli</option>
                    <option value="dizel">Dizel</option>
                </select>

                <label for="motosiklet_yillik_mesafe">Yıllık Motosikletle Yapılan Mesafe (km):</label>
                <input type="text" id="motosiklet_yillik_mesafe" name="motosiklet_yillik_mesafe">

                <label>Yıllık Uçak Seyahatleri Sayısı:</label>
                <input type="text" name="turkiye_avrupa" placeholder="Türkiye/Avrupa">
                <input type="text" name="avrupa_amerika" placeholder="Avrupa/Amerika">
                <input type="text" name="turkiye_amerika" placeholder="Türkiye/Amerika">
                <input type="text" name="turkiye_uzakdogu" placeholder="Türkiye/Uzakdoğu">

                <button type="submit">Hesapla</button>
            </form>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
