import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self) -> None:
        self.kassapaate = Kassapaate()

    def test_kassapaate_on_olemassa(self):
        self.assertNotEqual(self.kassapaate, None)

    def test_kassapaatteessa_rahaa_aluksi(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_alussa_ei_asiakkaita_palveltu(self):
        self.assertEqual(self.kassapaate.edulliset+self.kassapaate.maukkaat, 0)

    def test_kateismaksu_maukkaalla(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(vaihtoraha, 100)

    def test_kateismaksu_ei_riita_maukkaalla(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(300)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(vaihtoraha, 300)

    def test_kateismaksu_edullisella(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(vaihtoraha, 260)

    def test_kateismaksu_ei_riita_edullisella(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(vaihtoraha, 200)

    def test_myytyjen_lounaiden_maara_kasvaa_kateisella(self):
        vaihtoraha1 = self.kassapaate.syo_maukkaasti_kateisella(500)
        vaihtoraha2 = self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat, 1)
    
    def test_asiakkaiden_maara_ei_kasva_kun_raha_ei_riita_kateisella(self):
        vaihtoraha1 = self.kassapaate.syo_maukkaasti_kateisella(100)
        vaihtoraha2 = self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kortillamaksu_maukkaalla(self):
        kortti = Maksukortti(1000)
        palaute = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(palaute, True)

    def test_kortillamaksu_ei_riita_maukkaalla(self):
        kortti = Maksukortti(100)
        palaute = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(palaute, False)

    def test_kortillamaksu_edullisella(self):
        kortti = Maksukortti(1000)
        palaute = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(palaute, True)
    
    def test_kortillamaksu_ei_riita_edullisella(self):
        kortti = Maksukortti(100)
        palaute = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(palaute, False)

    def test_kortilta_vahennetaan_rahaa(self):
        kortti = Maksukortti(1000)
        palaute1 = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(kortti.saldo, 600)
        palaute2 = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(kortti.saldo, 360)

    def test_kortin_saldo_sailyy_kun_raha_ei_riita(self):
        kortti = Maksukortti(100)
        palaute1 = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(kortti.saldo, 100)
        palaute2 = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(kortti.saldo, 100)

    def test_kassan_rahamaara_ei_muutu_kortilla_maksaessa(self):
        kortti = Maksukortti(1000)
        palaute1 = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        palaute2 = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_asiakkaiden_maara_kasvaa_kortilla(self):
        kortti = Maksukortti(1000)
        palaute1 = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        palaute2 = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_asiakkaiden_maara_ei_kasva_kun_raha_ei_riita_kortilla(self):
        kortti = Maksukortti(100)
        palaute1 = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        palaute2 = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kortille_lataaminen_toimii(self):
        kortti = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(kortti, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 101000)
        self.assertEqual(kortti.saldo, 2000)

    def test_kortille_ei_voi_ladata_negatiivista(self):
        kortti = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(kortti,-1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(kortti.saldo, 1000)