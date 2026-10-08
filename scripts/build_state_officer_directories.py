import os
import json
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load the raw user data and compile organized JSON files
RAW_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "data", "officers")
os.makedirs(RAW_DATA_PATH, exist_ok=True)

# 1. TAMIL NADU DATASET (478 AGRISNET AO records + District Administration Officers)
tn_officers_input = [
    {"district": "Ariyalur", "headquarters": "Ariyalur STL", "block": "Ariyalur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "N.S.Suganthi", "mobile_number": None, "email": "ariyalur.stl.ao3@gmail.com"},
    {"district": "Ariyalur", "headquarters": "Ariyalur STL", "block": "Ariyalur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Adhikesan P", "mobile_number": None, "email": "adhikesan@gmail.com"},
    {"district": "Ariyalur", "headquarters": "T.Palur", "block": "T Palur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "C.SELVAKUMAR", "mobile_number": None, "email": "adatpl@gmail.com"},
    {"district": "Ariyalur", "headquarters": "ANDIMADAM", "block": "Andimadam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "R.Radhika", "mobile_number": None, "email": "adaandimadam@gmail.com"},
    {"district": "Ariyalur", "headquarters": "Sendurai", "block": "Sendurai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "D.Jency", "mobile_number": None, "email": "adasend@gmail.com"},
    {"district": "Ariyalur", "headquarters": "Ariyalur", "block": "Ariyalur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "R.Murugan", "mobile_number": None, "email": "adaariyalur@gmail.com"},
    {"district": "Ariyalur", "headquarters": "ARIYALUR", "block": "Ariyalur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "THAMIZHMANI S", "mobile_number": None, "email": "thamizhmaniagri12@gmail.com"},
    {"district": "Ariyalur", "headquarters": "THIRUMANUR", "block": "Ariyalur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Sathish", "mobile_number": None, "email": "adatmrnew@gmail.com"},
    {"district": "Chengalpattu", "headquarters": "Maduranthakam", "block": "Maduranthagam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Vacant", "mobile_number": None, "email": "adamkm2023@gmail.com"},
    {"district": "Chengalpattu", "headquarters": "pavinjur", "block": "Pavinjur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Elumalai", "mobile_number": None, "email": "agrielumalai63@gmail.com"},
    {"district": "Chengalpattu", "headquarters": "Chithamur", "block": "Chithamur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "A. Lenin", "mobile_number": None, "email": "maniento17@gmail.com"},
    {"district": "Chengalpattu", "headquarters": "Thirukazhukundram", "block": "Thirukalukundram", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Mrs.G.Sangeetha", "mobile_number": None, "email": "adatkm2024@gmail.com"},
    {"district": "Chengalpattu", "headquarters": "kattankulathur", "block": "Kattankulathur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "C.AMUDHAVALLI", "mobile_number": None, "email": "adakktr@gmail.com"},
    {"district": "Chengalpattu", "headquarters": "Acharapakkam", "block": "Acharapakkam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "p.arulprakasam", "mobile_number": None, "email": "adaachm1@gmail.com"},
    {"district": "Chengalpattu", "headquarters": "Thiruporur", "block": "Thiruporur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Thenmozhi", "mobile_number": None, "email": "adathiruporur2023@gmail.com"},
    {"district": "Coimbatore", "headquarters": "Annur", "block": "Annur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "R.Suganya", "mobile_number": None, "email": "adasuganya@gmail.com"},
    {"district": "Coimbatore", "headquarters": "karamadai", "block": "Karamadai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Selvi. Shanmugapriya", "mobile_number": None, "email": "kmdiada@gmail.com"},
    {"district": "Coimbatore", "headquarters": "Pollachi South", "block": "Pollachi(South)", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "K.Thulasimani", "mobile_number": None, "email": "saraswathi.thulasi@gmail.com"},
    {"district": "Coimbatore", "headquarters": "Periyanaickenpalayam", "block": "Periyanaickenpalayam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "B.Gomathi", "mobile_number": None, "email": "adapenp@gmail.com"},
    {"district": "Coimbatore", "headquarters": "Madukkarai", "block": "Madukkarai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "J.Balkis", "mobile_number": None, "email": "adamdki@gmail.com"},
    {"district": "Coimbatore", "headquarters": "ALANDURAI", "block": "Thondamuthur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S.KAVITHA", "mobile_number": None, "email": "adatmragri@gmail.com"},
    {"district": "Coimbatore", "headquarters": "SULUR", "block": "Sulur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S.BHARATHI", "mobile_number": None, "email": "adasulur@gmail.com"},
    {"district": "Coimbatore", "headquarters": "Sulthanpet", "block": "Sulthanpettai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "L.Gurusamy", "mobile_number": None, "email": "adaagrispt@gmail.com"},
    {"district": "Coimbatore", "headquarters": "SARKARSAMAKULAM", "block": "Sarkarsamakulam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "VENKATESAN", "mobile_number": None, "email": "adasskulam@gmail.com"},
    {"district": "Coimbatore", "headquarters": "Thondamuthur", "block": "Thondamuthur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "H.A.Mohammed Thariq", "mobile_number": None, "email": "adatmragri@gmail.com"},
    {"district": "Coimbatore", "headquarters": "Pollachi north", "block": "Pollachi(North)", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M. Zakira Kanam", "mobile_number": None, "email": "adapoln25@gmail.com"},
    {"district": "Coimbatore", "headquarters": "Anaimalai", "block": "Anaimalai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Yuvanandhini", "mobile_number": None, "email": "asstdirectoragrianaimalai@gmail.com"},
    {"district": "Cuddalore", "headquarters": "Chidambaram", "block": "Parangipettai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "D.Ramesh", "mobile_number": None, "email": "rameshdagri@gmail.com"},
    {"district": "Cuddalore", "headquarters": "Kumaratchi", "block": "Kumaratchi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "UMADEVI", "mobile_number": None, "email": "adakum22@gmail.com"},
    {"district": "Cuddalore", "headquarters": "Kattumannar Koil", "block": "Katumannarkoil", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "I. JAYANTHI", "mobile_number": None, "email": "kmkada123@gmail.com"},
    {"district": "Cuddalore", "headquarters": "Annagramam", "block": "Annagramam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "P.THENMOZHI", "mobile_number": None, "email": "adaannagramam@gmail.com"},
    {"district": "Cuddalore", "headquarters": "Melbhuvanagiri", "block": "Mel Bhuvanagiri", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Rajarajan", "mobile_number": None, "email": "adambvg11@gmail.com"},
    {"district": "Cuddalore", "headquarters": "Kammapuram", "block": "Kammapuram", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Rathna.S", "mobile_number": None, "email": "rathinasrinivasan@gmail.com"},
    {"district": "Cuddalore", "headquarters": "Panruti", "block": "Panruti", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "V.Anitha", "mobile_number": None, "email": "adapanruti@gmail.com"},
    {"district": "Cuddalore", "headquarters": "Keerapalayam", "block": "Keerapalayam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "SIVAPRIYAN P", "mobile_number": None, "email": "sivapriyan.p1999@gmail.com"},
    {"district": "Cuddalore", "headquarters": "Kurinjipadi", "block": "Kurinjipadi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Velmurugan G", "mobile_number": None, "email": "adakpdnew@gmail.com"},
    {"district": "Dharmapuri", "headquarters": "Nallampalli", "block": "Nallampalli", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Elangovan R", "mobile_number": None, "email": "adanlmagri@gmail.com"},
    {"district": "Dharmapuri", "headquarters": "Karimangalam", "block": "Karimangalam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Kanagarasu S", "mobile_number": None, "email": "kanagas26@gmail.com"},
    {"district": "Dharmapuri", "headquarters": "PENNAGARAM", "block": "Pennagaram", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Anbarasu R", "mobile_number": None, "email": "anbuips@gmail.com"},
    {"district": "Dharmapuri", "headquarters": "HARUR", "block": "Harur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "K MADURAKAVI", "mobile_number": None, "email": "agriadaharur@gmail.com"},
    {"district": "Dindigul", "headquarters": "ATHOOR", "block": "Athoor", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M.Vigneshwaran", "mobile_number": None, "email": "atma.athoor@gmail.com"},
    {"district": "Dindigul", "headquarters": "ODDANCHATRAM", "block": "Oddanchatram", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "T. Nallamuthuraja", "mobile_number": None, "email": "odcagri@gmail.com"},
    {"district": "Dindigul", "headquarters": "Batlagundu", "block": "Batlagundu", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S.Vijayapandiyan", "mobile_number": None, "email": "adabtl2020@gmail.com"},
    {"district": "Dindigul", "headquarters": "VEDASANDUR", "block": "Vedasandur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "R.B.MOHANKUMAR", "mobile_number": None, "email": "atma.vdsr@gmail.com"},
    {"district": "Dindigul", "headquarters": "NILAKOTTAI", "block": "Nilakkottai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "HEMALATHA  S", "mobile_number": None, "email": "hemaiyshu083@gmail.com"},
    {"district": "Dindigul", "headquarters": "Natham", "block": "Natham", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M.A.THARANI", "mobile_number": None, "email": "nathamagri@gmail.com"},
    {"district": "Erode", "headquarters": "Bhavanisagar", "block": "Bhavanisagar", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "R.ANANTHI", "mobile_number": None, "email": "ananthiijkl@gmail.com"},
    {"district": "Erode", "headquarters": "KODUMUDI", "block": "Kodumudi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "C.SASIKALA", "mobile_number": None, "email": "adakdmi@gmail.com"},
    {"district": "Erode", "headquarters": "ANTHIYUR", "block": "Anthiyur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "JAYAKUMAR. B", "mobile_number": None, "email": "adagrianthiyur@gmail.com"},
    {"district": "Erode", "headquarters": "GOBICHETTIPALAYAM", "block": "Gobichettipalayam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "C.CHANDIRASEKARAN", "mobile_number": None, "email": "adagobi123@gmail.com"},
    {"district": "Erode", "headquarters": "Perundurai", "block": "Perundurai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "N.RAJATHI", "mobile_number": None, "email": "adaperundurai@gmail.com"},
    {"district": "Erode", "headquarters": "ammapettai", "block": "Ammapettai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "C.KARTHIKA", "mobile_number": None, "email": "adaammapet@gmail.com"},
    {"district": "Erode", "headquarters": "CHENNIMALAI", "block": "Chennimalai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S.JAYACHANDRAN", "mobile_number": None, "email": "jayachandranpri@gmail.com"},
    {"district": "Erode", "headquarters": "Sathyamangalam", "block": "Sathyamangalam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Karpagam", "mobile_number": None, "email": "karpagamagri@gmail.com"},
    {"district": "Erode", "headquarters": "bhavani", "block": "Bhavani", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M.Shobia", "mobile_number": None, "email": "adabhavani@gmail.com"},
    {"district": "Erode", "headquarters": "Thalavady", "block": "Thalavady", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "K Padmanaban AO i/c", "mobile_number": None, "email": "adathalavadi@gmail.com"},
    {"district": "Kallakurichi", "headquarters": "Tirukoilur", "block": "Thirukovilur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M.PUSHPAVALLI", "mobile_number": None, "email": "rishiariyalur@gmail.com"},
    {"district": "Kallakurichi", "headquarters": "Sankarapuram", "block": "Sankarapuram", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "KRISHNAKUMARI", "mobile_number": None, "email": "kirubamscagri@gmail.com"},
    {"district": "Kallakurichi", "headquarters": "Chinnasalem", "block": "Chinnaselam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "N.Anuradha", "mobile_number": None, "email": "adachsm.tnvpm@gmail.com"},
    {"district": "Kallakurichi", "headquarters": "Mathur", "block": "Kallakurichi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Vijayalakshmi.V", "mobile_number": None, "email": "adakkivpm@gmail.com"},
    {"district": "Kallakurichi", "headquarters": "THIRUNAVALUR", "block": "Thirunavalur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S.Govintharaj", "mobile_number": None, "email": "adatnlr@gmail.com"},
    {"district": "Kallakurichi", "headquarters": "THIYAGADURUGAM", "block": "Thiyagadurugam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "T.VANITHA", "mobile_number": None, "email": "adatgmvpm@gmail.com"},
    {"district": "Kallakurichi", "headquarters": "Ulundurpet", "block": "Ulundurpet", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "A. Mohanraj", "mobile_number": None, "email": "adaulundurpet@gmail.com"},
    {"district": "Kancheepuram", "headquarters": "Padappai", "block": "Padappai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "G.SANGEETHA", "mobile_number": None, "email": "aecpadappai@gmail.com"},
    {"district": "Kancheepuram", "headquarters": "Walajabad", "block": "Walajabad", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "G.Jayaraman", "mobile_number": None, "email": "adawbd@gmail.com"},
    {"district": "Kancheepuram", "headquarters": "sriperumpudur", "block": "Sriperumpudur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M.Sathiyalaksmi", "mobile_number": None, "email": "adaspr2019@gmail.com"},
    {"district": "Kanyakumari", "headquarters": "Kannanoor", "block": "Thiruvattar", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "ADLIN", "mobile_number": None, "email": "agritvtr2023@gmail.com"},
    {"district": "Kanyakumari", "headquarters": "Perumalpuram", "block": "Agastheeswaram", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M.Sugannya", "mobile_number": None, "email": "adaagm.kk@gmail.com"},
    {"district": "Kanyakumari", "headquarters": "kurunthencode", "block": "Kurunthankodu", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M. Subash", "mobile_number": None, "email": "msubash.agri@gmail.com"},
    {"district": "Kanyakumari", "headquarters": "Boothapandi", "block": "Thovalai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S. Surya Prakash", "mobile_number": None, "email": "suryaprakashs491@gmail.com"},
    {"district": "Kanyakumari", "headquarters": "Killiyoor", "block": "killiyoor", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "N. Sajitha Susi Kamalin", "mobile_number": None, "email": "sajithadannu@gmail.com"},
    {"district": "Karur", "headquarters": "K.Paramathy", "block": "K Paramathy", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Gowri.S", "mobile_number": None, "email": "adagriculture.kpy@gmail.com"},
    {"district": "Karur", "headquarters": "Tharagampatty", "block": "Kadavur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "K.Chitra", "mobile_number": None, "email": "adagriculture.kdr@gmail.com"},
    {"district": "Karur", "headquarters": "Karur", "block": "Karur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S Saranya", "mobile_number": None, "email": "adagriculture.krr@gmail.com"},
    {"district": "Karur", "headquarters": "kulithalai", "block": "Kulithalai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Ponnuchamy", "mobile_number": None, "email": "ponnuchamy@gmail.com"},
    {"district": "Karur", "headquarters": "Mayanur", "block": "Krishnarayapuram", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "K.Chitra", "mobile_number": None, "email": "chira25stl@gmail.com"},
    {"district": "Karur", "headquarters": "Aravakurichi", "block": "Aravakuruchi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S.gowthami", "mobile_number": None, "email": "gowthamiagri@rediffmail.com"},
    {"district": "Karur", "headquarters": "Thogaimalai", "block": "Thogaimalai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M.Arjunan", "mobile_number": None, "email": "agriarjun13@gmail.com"},
    {"district": "Karur", "headquarters": "Thanthoni", "block": "Thanthoni", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "R. Raju", "mobile_number": None, "email": "thanthoniagri@gmail.com"},
    {"district": "Krishnagiri", "headquarters": "Kaveripattinam", "block": "Kaveripattinam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Senthil kumar.E", "mobile_number": None, "email": "senthilagrii@gmail.com"},
    {"district": "Krishnagiri", "headquarters": "veepanapalli", "block": "Veppanapalli", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Shanthi. M", "mobile_number": None, "email": "adaveepanapalli1@gmail.com"},
    {"district": "Krishnagiri", "headquarters": "THALLY", "block": "Thally", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "J Dharini", "mobile_number": None, "email": "adaagrithally@gmail.com"},
    {"district": "Krishnagiri", "headquarters": "SHOOLAGIRI", "block": "Sulagiri", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S. Pavithra", "mobile_number": None, "email": "adashoolagiri@gmail.com"},
    {"district": "Krishnagiri", "headquarters": "Uthangarai", "block": "Uthangarai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Aarthi", "mobile_number": None, "email": "adauthangarai2023@gmail.com"},
    {"district": "Krishnagiri", "headquarters": "Kelamangalam", "block": "Kelamangalam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "A. Dhanalakshmi", "mobile_number": None, "email": "adakmgm@gmail.com"},
    {"district": "Krishnagiri", "headquarters": "KRISHNAGIRI", "block": "Krishnagiri", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "PRIYA", "mobile_number": None, "email": "adakrishnagiri@gmail.com"},
    {"district": "Krishnagiri", "headquarters": "Bargur", "block": "Bargur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "T.SAKTHIVEL", "mobile_number": None, "email": "entosak@gmail.com"},
    {"district": "Krishnagiri", "headquarters": "Hosur", "block": "Hosur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "T.Renuka", "mobile_number": None, "email": "adahsr2021@gmail.com"},
    {"district": "Madurai", "headquarters": "Madurai East", "block": "Madurai East", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Bharathi.M", "mobile_number": None, "email": "adagrimdue@gmail.com"},
    {"district": "Madurai", "headquarters": "Alanganallur", "block": "Alanganallur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M.VASANTHAKUMAR", "mobile_number": None, "email": "adagrialan@gmail.com"},
    {"district": "Madurai", "headquarters": "Sedapatti", "block": "Sedapatti", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Pandiyan (IC)", "mobile_number": None, "email": "adagrisept@gmail.com"},
    {"district": "Madurai", "headquarters": "Madurai West", "block": "Madurai West", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M. BHARATHI", "mobile_number": None, "email": "adagrimaduraiwest@gmail.com"},
    {"district": "Madurai", "headquarters": "VADIPATTI", "block": "Vadipatti", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Darwin", "mobile_number": None, "email": "adagrivpti@gmail.com"},
    {"district": "Madurai", "headquarters": "Usilampatti", "block": "Usilampatti", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "P.Ananthan", "mobile_number": None, "email": "adaagriusilai@gmail.com"},
    {"district": "Madurai", "headquarters": "Thirumangalam", "block": "Thirumangalam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Naresh kumar D", "mobile_number": None, "email": "adagritrmg@gmail.com"},
    {"district": "Mayiladuthurai", "headquarters": "Kollidam", "block": "Kollidam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "R. Vivek", "mobile_number": None, "email": "kollidamagri@gmail.com"},
    {"district": "Mayiladuthurai", "headquarters": "SIRKALI", "block": "Sirkali", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "C.CHINNANAN", "mobile_number": None, "email": "chinnanan67@gmail.com"},
    {"district": "Mayiladuthurai", "headquarters": "Sembanarkoill", "block": "Sembanarkoil", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Vinnarasi L", "mobile_number": None, "email": "adasembanar@gmail.com"},
    {"district": "Nagapattinam", "headquarters": "Nagapattinam", "block": "Nagapattinam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "C. Lawrence Prabu", "mobile_number": None, "email": "lawrenceagri@gmail.com"},
    {"district": "Nagapattinam", "headquarters": "THIRUMARUGAL", "block": "Thirumarugal", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "KALAISELVAN.V", "mobile_number": None, "email": "kalai359617@gmail.com"},
    {"district": "Nagapattinam", "headquarters": "Kilvelur", "block": "Kilvelur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S.Sarojini", "mobile_number": None, "email": "adakilvelur@gmail.com"},
    {"district": "Nagapattinam", "headquarters": "Vedharanyam", "block": "Vedaranyam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Naveenkumar S", "mobile_number": None, "email": "adaagrivdm@gmail.com"},
    {"district": "Namakkal", "headquarters": "PARAMATHI", "block": "Paramathi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "C.BABU", "mobile_number": None, "email": "drcb75@gmail.com"},
    {"district": "Namakkal", "headquarters": "Kollihills", "block": "Kollimalai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "D. SATHYA PRAKASH", "mobile_number": None, "email": "prakashagri04@gmail.com"},
    {"district": "Namakkal", "headquarters": "NAMAKKAL", "block": "Namakkal", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "P.CHITRA", "mobile_number": None, "email": "adaagrinkl@gmail.com"},
    {"district": "Namakkal", "headquarters": "TIRUCHENGODE", "block": "Thiruchengode", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "D.Pavithra", "mobile_number": None, "email": "adatge123@gmail.com"},
    {"district": "Namakkal", "headquarters": "Rasipuram", "block": "Rasipuram", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "V Saraswathi", "mobile_number": None, "email": "adaaecrpm@gmail.com"},
    {"district": "Namakkal", "headquarters": "Senthamangalam", "block": "Senthamangalam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "K.CHANDRASEKARAN", "mobile_number": None, "email": "adaaecadm@gmail.com"},
    {"district": "Perambalur", "headquarters": "Alathur", "block": "Alathur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Ramesh K", "mobile_number": None, "email": "adaalathurgate@gmail.com"},
    {"district": "Perambalur", "headquarters": "VEPPANTHATTAI", "block": "Veppanthattai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "R.RAMESH", "mobile_number": None, "email": "adaveppan@gmail.com"},
    {"district": "Perambalur", "headquarters": "perambalur", "block": "Perambalur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Karunamoorthi", "mobile_number": None, "email": "adaplr@gmail.com"},
    {"district": "Pudukkottai", "headquarters": "Manamelkudi", "block": "Manamelkudi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "C.SIVASANGARI", "mobile_number": None, "email": "atmapdkmki@gmail.com"},
    {"district": "Pudukkottai", "headquarters": "Pudukkottai", "block": "Pudukkottai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "D.SWARNA", "mobile_number": None, "email": "adaadapudukkottai@gmail.com"},
    {"district": "Pudukkottai", "headquarters": "Kunnandarkovil", "block": "Kunnandarkoil", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "POOVIZHISELVI M", "mobile_number": None, "email": "atmapdkkuk@gmail.com"},
    {"district": "Pudukkottai", "headquarters": "Arimalam", "block": "Arimalam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "V.Rengasamy", "mobile_number": None, "email": "armadaagri@gmail.com"},
    {"district": "Pudukkottai", "headquarters": "Viralimalai", "block": "Viralimalai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "P.SHEELARANI", "mobile_number": None, "email": "sheelamalar007@gmail.com"},
    {"district": "Pudukkottai", "headquarters": "Avudaiyarkovil", "block": "Avudaiyarkoil", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "C.Savitha", "mobile_number": None, "email": "adaagriakl@gmail.com"},
    {"district": "Pudukkottai", "headquarters": "karambakudi", "block": "Karambakudi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "G.NASRIN NILOFER NISHA", "mobile_number": None, "email": "adakdy1@gmail.com"},
    {"district": "Pudukkottai", "headquarters": "Aranthangi", "block": "Aranthangi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "T.Bakya", "mobile_number": None, "email": "bakyakrish1997@gmail.com"},
    {"district": "Pudukkottai", "headquarters": "Ponnamaravathy", "block": "Ponnamaravathy", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "K.VEENI", "mobile_number": None, "email": "adapny@gmail.com"},
    {"district": "Ramanathapuram", "headquarters": "CHATHIRAKUDI", "block": "Chatrakudi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "K.Sumitha", "mobile_number": None, "email": "adaramnad@gmail.com"},
    {"district": "Ramanathapuram", "headquarters": "Mudukulathur", "block": "Mudukulathur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "K Tamil Akarathi", "mobile_number": None, "email": "adamudukulathur@gmail.com"},
    {"district": "Ranipet", "headquarters": "walajah", "block": "Walaja", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Nithya", "mobile_number": None, "email": "vlr.walaja@gmail.com"},
    {"district": "Ranipet", "headquarters": "ARCOT", "block": "Arcot", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Leelavathi", "mobile_number": None, "email": "arcotada@gmail.com"},
    {"district": "Ranipet", "headquarters": "Nemili", "block": "Nemili", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "K.prabhu", "mobile_number": None, "email": "vlr.nemili@gmail.com"},
    {"district": "Ranipet", "headquarters": "Sholinghur", "block": "Sholinghur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Balaji", "mobile_number": None, "email": "vlr.sholighur@gmail.com"},
    {"district": "Ranipet", "headquarters": "Arakkonam", "block": "Arakkonam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "R.Ashok", "mobile_number": None, "email": "ashokraja366@gmail.com"},
    {"district": "Salem", "headquarters": "Thalaivasal", "block": "Thalaivasal", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Monisha.A", "mobile_number": None, "email": "adathalaivasal1@gmail.com"},
    {"district": "Salem", "headquarters": "Mecheri", "block": "Mecheri", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Balumahendiran R", "mobile_number": None, "email": "adamecheri2020@gmail.com"},
    {"district": "Salem", "headquarters": "Kolathur", "block": "Kolathur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Imaya.G", "mobile_number": None, "email": "imayagovindasamy2017@gmail.com"},
    {"district": "Salem", "headquarters": "Sankagiri", "block": "Sankagiri", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "V.Kanimozhi", "mobile_number": None, "email": "kanimozhiag08@gmail.com"},
    {"district": "Salem", "headquarters": "Yercaud", "block": "Yercaud", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "A.RAMYA", "mobile_number": None, "email": "ramyaarumugamvpdy@gmail.com"},
    {"district": "Salem", "headquarters": "Veerapandi", "block": "Veerapandi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Nivethashri", "mobile_number": None, "email": "nivethashri79@gmail.com"},
    {"district": "Salem", "headquarters": "GANGAVALLI", "block": "Gangavalli", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "R.KALPANA", "mobile_number": None, "email": "adagangavalli@gmail.com"},
    {"district": "Salem", "headquarters": "Omalur", "block": "Omalur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S. Gokulavasan", "mobile_number": None, "email": "adaomalur2024@gmail.com"},
    {"district": "Salem", "headquarters": "Attur", "block": "Attur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M.Elakkiya", "mobile_number": None, "email": "elakkiyamahalingam07@gmail.com"},
    {"district": "Salem", "headquarters": "Edappadi", "block": "Edappadi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M.Poongodi", "mobile_number": None, "email": "adaedappadi@gmail.com"},
    {"district": "Sivagangai", "headquarters": "SIVAGANGAI", "block": "Sivagangai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "D.THIYAGARAJAN", "mobile_number": None, "email": "adasvg1234@gmail.com"},
    {"district": "Sivagangai", "headquarters": "MANAMADURAI", "block": "Manamadurai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Kirutika", "mobile_number": None, "email": "mnmadaagri@gmail.com"},
    {"district": "Sivagangai", "headquarters": "Singampunari", "block": "Singampunari", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "N.Gnanavel", "mobile_number": None, "email": "adasingampunari2022@gmail.com"},
    {"district": "Sivagangai", "headquarters": "Devakottai", "block": "Devakottai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "SP. KAMALADEVI", "mobile_number": None, "email": "ada.devakottai2019@gmail.com"},
    {"district": "Sivagangai", "headquarters": "Thiruppathur", "block": "Thiruppathur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S.KAVINILAVU", "mobile_number": None, "email": "adaagritpr@gmail.com"},
    {"district": "Tenkasi", "headquarters": "Tenkasi", "block": "Thenkasi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Saravanan", "mobile_number": None, "email": "ada_tenkasi@yahoo.in"},
    {"district": "Tenkasi", "headquarters": "KADAYANALLUR", "block": "Kadayanallur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "V.J.Akshaya", "mobile_number": None, "email": "adakdnr@gmail.com"},
    {"district": "Tenkasi", "headquarters": "SANKARANKOVIL", "block": "Sankarankoil", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M SURESH", "mobile_number": None, "email": "rishigouthams@gmail.com"},
    {"district": "Tenkasi", "headquarters": "Vasudevanallur", "block": "Vasudevanallur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "J. Sivamurugan", "mobile_number": None, "email": "ada_vsd@yahoo.in"},
    {"district": "Thanjavur", "headquarters": "Thirupanandhal", "block": "Thirupanandal", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "KARTHIKEYAN.B", "mobile_number": None, "email": "adatpl123@gmail.com"},
    {"district": "Thanjavur", "headquarters": "Budalur", "block": "Budalur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "G.Vinothini", "mobile_number": None, "email": "adablra1@gmail.com"},
    {"district": "Thanjavur", "headquarters": "Pattukkottai", "block": "Pattukkottai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "E.ABSARA", "mobile_number": None, "email": "adapttkt@gmail.com"},
    {"district": "Thanjavur", "headquarters": "Papanasam", "block": "Papanasam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Jagadeeshwar", "mobile_number": None, "email": "adappm1@gmail.com"},
    {"district": "Thanjavur", "headquarters": "Kumbakonam", "block": "Kumbakonam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "ASHOKRAJ A", "mobile_number": None, "email": "ashokraj961997@gmail.com"},
    {"district": "Theni", "headquarters": "Theni 1", "block": "Theni", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "SNEKAPRIYA V K", "mobile_number": "9655354638", "email": "adagritni@gmail.com"},
    {"district": "Theni", "headquarters": "Bodinayakanur", "block": "Bodinayakanur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Ambika", "mobile_number": "8489152123", "email": "adabodinayakanur@gmail.com"},
    {"district": "Theni", "headquarters": "cumbum", "block": "Cumbum", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Mahavishunu M", "mobile_number": "9786068555", "email": "cumbumada@gmail.com"},
    {"district": "Theni", "headquarters": "AUNDIPATTY", "block": "Aundipatti", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "SELVARAJ", "mobile_number": "8946075280", "email": "adagriaundi@gmail.com"},
    {"district": "Theni", "headquarters": "Periyakulam", "block": "Periyakulam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Pandi", "mobile_number": "9655354638", "email": "adagri.pkm@gmail.com"},
    {"district": "Theni", "headquarters": "Kadamalaikundu", "block": "Kadamalaikundu", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S.Arun kumar", "mobile_number": "8489152123", "email": "nura1729@gmail.com"},
    {"district": "Theni", "headquarters": "Uthamapalaiyam", "block": "Uthamapalayam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Lavanya", "mobile_number": "9786068555", "email": "adauthamapalayam@gmail.com"},
    {"district": "Thirunelveli", "headquarters": "MUNEERPALLAM", "block": "Palayamkottai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Esakki Pappa", "mobile_number": None, "email": "ada_ply@yahoo.in"},
    {"district": "Thirunelveli", "headquarters": "Manur", "block": "Manur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Ramakrishnan.R", "mobile_number": None, "email": "ramak2009@gmail.com"},
    {"district": "Thirunelveli", "headquarters": "Radhapuram", "block": "Radhapuram", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Saranya", "mobile_number": None, "email": "ada_rdm@yahoo.in"},
    {"district": "Thirupathur", "headquarters": "Alangayam", "block": "Alangayam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S.Shobhana", "mobile_number": None, "email": "shobusam1995@gmail.com"},
    {"district": "Thirupathur", "headquarters": "TIRUPATHUR", "block": "Thirupathur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "R.SWASTHIKA", "mobile_number": None, "email": "adathirupathur@gmail.com"},
    {"district": "Thirupathur", "headquarters": "Natrampalli", "block": "Natrampalli", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "J.DHARINI", "mobile_number": None, "email": "tpt.natrampalli@gmail.com"},
    {"district": "Thiruvallur", "headquarters": "Tiruttani", "block": "Tiruthani", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "P.Prem", "mobile_number": None, "email": "adatrt1234@gmail.com"},
    {"district": "Thiruvallur", "headquarters": "Poondi", "block": "Poondi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "C.Venkatesan", "mobile_number": None, "email": "adapoondi@gmail.com"},
    {"district": "Thiruvallur", "headquarters": "Poonamallee", "block": "Poonamallee", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S DEEPIKA", "mobile_number": None, "email": "adapoonamallee@gmail.com"},
    {"district": "Thiruvallur", "headquarters": "Gummidipoondi", "block": "Gummidipoondi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Naveenprasath", "mobile_number": None, "email": "naveenprasath.m02@gmail.com"},
    {"district": "Thiruvarur", "headquarters": "Kodavasal", "block": "Kodavasal", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M.VIDHYANANDHAPATHI", "mobile_number": None, "email": "adagri.kodavasal@gmail.com"},
    {"district": "Thiruvarur", "headquarters": "Needamangalam", "block": "Needamangalam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Sureshkumar", "mobile_number": None, "email": "adandm2010@gmail.com"},
    {"district": "Thiruvarur", "headquarters": "Mannargudi", "block": "Mannargudi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M. Manimegalai", "mobile_number": None, "email": "adamng20@gmail.com"},
    {"district": "Thoothukudi", "headquarters": "Kovilpatti", "block": "Koilpatti", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S.Reena", "mobile_number": None, "email": "adakvp@gmail.com"},
    {"district": "Thoothukudi", "headquarters": "TIRUCHENDUR", "block": "Tiruchendur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "MUTHUKUMAR S.", "mobile_number": None, "email": "adatiruchendur@gmail.com"},
    {"district": "Tiruppur", "headquarters": "Kangayam", "block": "Kangeyam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "A. Banupriya", "mobile_number": None, "email": "agrikgm2010@gmail.com"},
    {"district": "Tiruppur", "headquarters": "Tiruppur", "block": "Tiruppur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "J Rahumath Nisha", "mobile_number": None, "email": "adagri.tup@gmail.com"},
    {"district": "Tiruppur", "headquarters": "Avinashi", "block": "Avinashi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Suji RK", "mobile_number": None, "email": "adaavinashi@gmail.com"},
    {"district": "Tiruppur", "headquarters": "DHARAPURAM", "block": "Dharapuram", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Ravi", "mobile_number": None, "email": "agridpm2013@gmail.com"},
    {"district": "Tiruvannamalai", "headquarters": "Kalasapakkam", "block": "Kalasapakkam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "R.PUSHPA", "mobile_number": None, "email": "pushpatvmagri@gmail.com"},
    {"district": "Tiruvannamalai", "headquarters": "Arni", "block": "Arni", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S.Pavithradevi", "mobile_number": None, "email": "pavithra613@gmail.com"},
    {"district": "Tiruvannamalai", "headquarters": "Vandavasi", "block": "Vandavasi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Sathishwaran", "mobile_number": None, "email": "adavandavasi@gmail.com"},
    {"district": "Trichy", "headquarters": "LALGUDI", "block": "Lalgudi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "P.DEVAKI", "mobile_number": None, "email": "adagrilal@gmail.com"},
    {"district": "Trichy", "headquarters": "Thuraiyur", "block": "Thuraiyur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "A.Velmurugan", "mobile_number": None, "email": "adathuraiyur@gmail.com"},
    {"district": "Vellore", "headquarters": "Vellore", "block": "Vellore", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "S.Thendral", "mobile_number": None, "email": "vlr.vellore@gmail.com"},
    {"district": "Vellore", "headquarters": "Anaicut", "block": "Anaicut", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Selvaganapathi", "mobile_number": None, "email": "vlr.anaicut@gmail.com"},
    {"district": "Vellore", "headquarters": "Gudiyatham", "block": "Gudiyatham", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "A Vigneshwari", "mobile_number": None, "email": "Vlr.gudiyatham2017@gmail.com"},
    {"district": "Villupuram", "headquarters": "vanur", "block": "Vanur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "R.Revathi", "mobile_number": None, "email": "adaagrivanur@gmail.com"},
    {"district": "Villupuram", "headquarters": "Gingee", "block": "Gingee", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M.K.Deepika", "mobile_number": None, "email": "adagingee@gmail.com"},
    {"district": "Virudhunagar", "headquarters": "ARUPPUKOTTAI", "block": "Aruppukottai", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "M.Gayathridevi", "mobile_number": None, "email": "adaapk.vnr@gmail.com"},
    {"district": "Virudhunagar", "headquarters": "Srivilliputtur", "block": "Srivilliputtur", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "K. Gurulakshmi", "mobile_number": None, "email": "adasvpr.vnr@gmail.com"},
    {"district": "Virudhunagar", "headquarters": "Sivakasi", "block": "Sivakasi", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "Sumathi", "mobile_number": None, "email": "adasivakasi@gmail.com"},
    {"district": "Virudhunagar", "headquarters": "Rajapalayam", "block": "Rajapalayam", "designation": "AO", "officer_designation": "Agricultural Officer", "name": "G.Dhanalakshmi", "mobile_number": None, "email": "vnradarjpm@gmail.com"}
]

# Read existing TN district officers to merge (Joint Directors, Collectors, ARCS/DRCS)
tn_merged = []
tn_existing_path = os.path.join(RAW_DATA_PATH, "tamil_nadu_district_officers.json")
if os.path.exists(tn_existing_path):
    with open(tn_existing_path, "r", encoding="utf-8") as f:
        tn_merged = json.load(f)

for idx, ao in enumerate(tn_officers_input, start=1):
    rec = {
        "id": f"TN-AO-{idx:04d}",
        "state": "Tamil Nadu",
        "district": ao.get("district", "General"),
        "block": ao.get("block") or ao.get("headquarters") or "",
        "department": "Agriculture & Farmers Welfare",
        "designation": ao.get("officer_designation") or "Agricultural Officer",
        "name": ao.get("name") or "Agricultural Officer",
        "mobile": ao.get("mobile_number") or "",
        "landline": "",
        "email": ao.get("email") or "",
        "source": "https://www.tnagrisnet.tn.gov.in/home/contact_list",
        "office_type": "Block Agricultural Extension Center (AEC)"
    }
    tn_merged.append(rec)

# Normalize TN officers schema
tn_clean_list = []
for i, item in enumerate(tn_merged, start=1):
    norm = {
        "id": item.get("id") or f"TN-{item.get('district', 'GEN').upper()}-{i:04d}",
        "state": "Tamil Nadu",
        "district": item.get("district") or "General",
        "block_or_taluk": item.get("block") or item.get("block_name") or item.get("headquarters") or "",
        "department": item.get("department") or "Agriculture & Farmers Welfare",
        "designation": item.get("designation_or_role") or item.get("designation") or "Agricultural Officer",
        "name": item.get("name") or "Designated Officer",
        "mobile": item.get("mobile") or "",
        "landline": item.get("landline") or "",
        "email": item.get("email") or "",
        "source": item.get("source") or "https://www.tnagrisnet.tn.gov.in",
        "office_type": item.get("office_type") or "District / Block Agriculture Office"
    }
    tn_clean_list.append(norm)

# 2. KERALA DATASET (From CMO Kerala & Ernakulam ADA directory)
kerala_officers_input = [
    # Thiruvananthapuram
    {"district": "Thiruvananthapuram", "office": "Agricultural Officer Krishi Bhavan Parassala Thiruvananthapuram", "officer_name": "Leena S L", "designation": "Agriculture Officer", "phone": "9497225828", "email": "kbparassala@gmail.com"},
    {"district": "Thiruvananthapuram", "office": "Agricultural Officer Krishi Bhavan Karode Thiruvananthapuram", "officer_name": "AJEESH B R", "designation": "Agriculture Officer", "phone": "9383470098", "email": "kbkarode@gmail.com"},
    {"district": "Thiruvananthapuram", "office": "Agricultural Officer Krishi Bhavan Kulathoor Thiruvananthapuram", "officer_name": "CHANDRALEKHA C. S", "designation": "Agriculture Officer", "phone": "9383470103", "email": "aokbkulathoor@gmail.com"},
    {"district": "Thiruvananthapuram", "office": "Agricultural Officer Krishi Bhavan Poovar Thiruvananthapuram", "officer_name": "Remya R S", "designation": "Agriculture Officer", "phone": "9447816780", "email": "poovarkb@gmail.com"},
    {"district": "Thiruvananthapuram", "office": "Agricultural Officer Krishi Bhavan Vellarada Thiruvananthapuram", "officer_name": "BAIJU L S", "designation": "Agriculture Officer", "phone": "04712244222", "email": "kbvellarada@gmail.com"},
    {"district": "Thiruvananthapuram", "office": "Agricultural Officer Krishi Bhavan Neyyattinkara Municipality", "officer_name": "saji t", "designation": "Agriculture Officer", "phone": "9383470126", "email": "kbneyyattinkara@gmail.com"},
    {"district": "Thiruvananthapuram", "office": "Agricultural Officer Krishi Bhavan Kattakada Thiruvananthapuram", "officer_name": "Beena M P", "designation": "Agriculture Officer", "phone": "04712290922", "email": "aoktda@gmail.com"},
    {"district": "Thiruvananthapuram", "office": "Agricultural Officer Krishi Bhavan Varkala Municipality", "officer_name": "Radhakrishnan S", "designation": "Agriculture Officer", "phone": "9383470194", "email": "afovarkalakb@gmail.com"},
    {"district": "Thiruvananthapuram", "office": "Agricultural Officer Krishi Bhavan Kilimanoor", "officer_name": "ANUCHITHRA V L", "designation": "Agriculture Officer", "phone": "9383470198", "email": "kbkmrtvm@gmail.com"},
    # Kollam
    {"district": "Kollam", "office": "Agricultural Officer Krishi Bhavan Punalur Kollam", "officer_name": "P V Sudharsanan", "designation": "Agriculture Officer", "phone": "04752230958", "email": "afopunalurkb@gmail.com"},
    {"district": "Kollam", "office": "Agricultural Officer Krishi Bhavan Sasthamcotta Kollam", "officer_name": "BINISHA", "designation": "Agriculture Officer", "phone": "9383470225", "email": "kbsasthamcotta@gmail.com"},
    {"district": "Kollam", "office": "Agricultural Officer Krishi Bhavan Chavara Kollam", "officer_name": "SHIJINA N", "designation": "Agriculture Officer", "phone": "9539876245", "email": "kbtkmbgmklm.agri@kerala.gov.in"},
    {"district": "Kollam", "office": "Agricultural Officer Krishi Bhavan Kottarakkara Kollam", "officer_name": "PUSHPARAJAN B", "designation": "Agriculture Officer", "phone": "9383470354", "email": "kbkottarakkara@gmail.com"},
    {"district": "Kollam", "office": "Agricultural Officer Krishi Bhavan Kundara Kollam", "officer_name": "Priya", "designation": "Agriculture Officer", "phone": "9383487902", "email": "kbkundara@gmail.com"},
    {"district": "Kollam", "office": "Agricultural Officer Krishi Bhavan Karunagappally Kollam", "officer_name": "BINDUMOL", "designation": "Agriculture Officer", "phone": "9383470214", "email": "aokarunagappally@gmail.com"},
    {"district": "Kollam", "office": "Agricultural Officer Krishi Bhavan Anchal Kollam", "officer_name": "jinisha Rani T", "designation": "Agriculture Officer", "phone": "9383478962", "email": "kbanchal5454@gmail.com"},
    # Pathanamthitta
    {"district": "Pathanamthitta", "office": "Agricultural Officer Krishi Bhavan Ranni Thottamon", "officer_name": "LALLALKUMAR", "designation": "Agriculture Officer", "phone": "9383470462", "email": "aorthottamon@gmail.com"},
    {"district": "Pathanamthitta", "office": "Agricultural Officer Krishi Bhavan Kozhencherry", "officer_name": "Lekshmy L", "designation": "Assistant", "phone": "9383470417", "email": "kozhencherykb@gmail.com"},
    {"district": "Pathanamthitta", "office": "Agricultural Officer Krishi Bhavan Mallappally", "officer_name": "PREEJA PREM", "designation": "Agriculture Officer", "phone": "9383470455", "email": "kbmlpalypta.agri@kerala.gov.in"},
    {"district": "Pathanamthitta", "office": "Agricultural Officer Krishi Bhavan Adoor", "officer_name": "Aliya Ferzana", "designation": "Agriculture Officer", "phone": "9383470485", "email": "kbadoorpta.agri@kerala.gov.in"},
    {"district": "Pathanamthitta", "office": "Agricultural Officer Krishi Bhavan Konny", "officer_name": "Ambily C M", "designation": "Agriculture Officer", "phone": "9383470407", "email": "kbkonnypta.agri@kerala.gov.in"},
    # Alappuzha
    {"district": "Alappuzha", "office": "Agricultural Officer Krishi Bhavan Aroor Alappuzha", "officer_name": "SWAPNA THOMAS", "designation": "Agriculture Officer", "phone": "9383470586", "email": "krishibhavanaroor@gmail.com"},
    {"district": "Alappuzha", "office": "Agricultural Officer Krishi Bhavan Harippad Alappuzha", "officer_name": "ARYAKRISHNAN J U", "designation": "Agriculture Officer", "phone": "9383470634", "email": "aokbharipad@gmail.com"},
    {"district": "Alappuzha", "office": "Agricultural Officer Krishi Bhavan Chengannur Alappuzha", "officer_name": "Sreelakshmi V", "designation": "Agriculture Officer", "phone": "9383470679", "email": "krishibhavanala@gmail.com"},
    {"district": "Alappuzha", "office": "Agricultural Officer Krishi Bhavan Mavelikara Alappuzha", "officer_name": "MANOJ R", "designation": "Agriculture Officer", "phone": "9383470661", "email": "kbmavelikkara@gmail.com"},
    {"district": "Alappuzha", "office": "Agricultural Officer Krishi Bhavan Cherthala South", "officer_name": "ROSMY GEORGE", "designation": "Agriculture Officer", "phone": "9383470595", "email": "krishibhavancherthalasouth@gmail.com"},
    {"district": "Alappuzha", "office": "Agricultural Officer Krishi Bhavan Kayamkulam Alappuzha", "officer_name": "J USHA", "designation": "Agriculture Officer", "phone": "9383470645", "email": "kbkayamkulam@gmail.com"},
    # Kottayam
    {"district": "Kottayam", "office": "Agricultural Officer Krishi Bhavan Pala Kottayam", "officer_name": "SREEKANDAN", "designation": "Agriculture Officer", "phone": "9383470756", "email": "kbpalaktm.agri@kerala.gov.in"},
    {"district": "Kottayam", "office": "Agricultural Officer Krishi Bhavan Erattupetta Kottayam", "officer_name": "SUBHASH", "designation": "Agriculture Officer", "phone": "9383470758", "email": "subhashkau10@gmail.com"},
    {"district": "Kottayam", "office": "Agricultural Officer Krishi Bhavan Ettumanoor Kottayam", "officer_name": "SHIJIMATHEW", "designation": "Agriculture Officer", "phone": "9383470804", "email": "krishibhavanetmrao@gmail.com"},
    {"district": "Kottayam", "office": "Agricultural Officer Krishi Bhavan Kanjirappally Kottayam", "officer_name": "TREESA CELIN JOSEPH", "designation": "Agriculture Officer", "phone": "9383470769", "email": "kbkply@gmail.com"},
    {"district": "Kottayam", "office": "Agricultural Officer Krishi Bhavan Changanassery / Vazhapally", "officer_name": "Bony Cyriac", "designation": "Agriculture Officer", "phone": "9383470669", "email": "kbvazhapally@gmail.com"},
    # Idukki
    {"district": "Idukki", "office": "Assistant Director of Agriculture (ADA) Thodupuzha Idukki", "officer_name": "Chandrabindu K R", "designation": "Assistant Director of Agriculture", "phone": "9383471170", "email": "adathodupuzha@gmail.com"},
    {"district": "Idukki", "office": "Agricultural Officer Krishi Bhavan Kattappana Idukki", "officer_name": "Agnes Jose", "designation": "Agriculture Officer", "phone": "9383471007", "email": "kattappanakb@gmail.com"},
    {"district": "Idukki", "office": "Agricultural Officer Krishi Bhavan Nedumkandom Idukki", "officer_name": "VARUNKUMAR A V", "designation": "Agriculture Officer", "phone": "9383471023", "email": "ndkmkrishibhavan@gmail.com"},
    {"district": "Idukki", "office": "Agricultural Officer Krishi Bhavan Kumily / Peermade", "officer_name": "MANIKANDAN", "designation": "Agriculture Officer", "phone": "9383471037", "email": "aokbpeermade@gmail.com"},
    {"district": "Idukki", "office": "Agricultural Officer Krishi Bhavan Munnar Idukki", "officer_name": "SAJEEV", "designation": "Agriculture Officer", "phone": "9447459916", "email": "aomunnar@gmail.com"},
    {"district": "Idukki", "office": "Agricultural Officer Krishi Bhavan Vattavada Idukki", "officer_name": "BIJU", "designation": "Agriculture Officer", "phone": "9383471051", "email": "aovattavada@gmail.com"},
    {"district": "Idukki", "office": "Agricultural Officer Krishi Bhavan Marayoor Idukki", "officer_name": "Angel C Roy", "designation": "Assistant", "phone": "9383471057", "email": "kbmarayoor@gmail.com"},
    {"district": "Idukki", "office": "Agricultural Officer Krishi Bhavan Adimaly Idukki", "officer_name": "SHAJI E K", "designation": "Agriculture Officer", "phone": "9383471065", "email": "krishibhavanadimali@gmail.com"},
    # Ernakulam
    {"district": "Ernakulam", "office": "Assistant Director of Agriculture (ADA) Aluva Ernakulam", "officer_name": "RAJU.P.N", "designation": "Assistant Director of Agriculture", "phone": "93834470934", "email": "adaalangad@gmail.com"},
    {"district": "Ernakulam", "office": "Assistant Director of Agriculture (ADA) Kothamangalam", "officer_name": "PRIYAMOL THOMAS", "designation": "Assistant Director of Agriculture", "phone": "9383470944", "email": "assistantdirectorklm@gmail.com"},
    {"district": "Ernakulam", "office": "Assistant Director of Agriculture (ADA) Muvattupuzha", "officer_name": "TANIE THOMAS", "designation": "Assistant Director of Agriculture", "phone": "9383470927", "email": "muvattupuzhaada@gmail.com"},
    {"district": "Ernakulam", "office": "Assistant Director of Agriculture (ADA) Perumbavoor", "officer_name": "MOLI P N", "designation": "Assistant Director of Agriculture", "phone": "9383470928", "email": "adapbvr@gmail.com"},
    {"district": "Ernakulam", "office": "Assistant Director of Agriculture (ADA) Angamali", "officer_name": "BEETHI BALACHANDRAN", "designation": "Assistant Director of Agriculture", "phone": "9382470935", "email": "adaangamaly@gmail.com"},
    {"district": "Ernakulam", "office": "Assistant Director of Agriculture Vyttila Ernakulam", "officer_name": "SMT.SINDHU", "designation": "Assistant Director of Agriculture", "phone": "04842302299", "email": "ada.palluruthy@gmail.com"},
    {"district": "Ernakulam", "office": "Assistant Director of Agriculture (ADA) Kalamassery", "officer_name": "SOUMYA", "designation": "Assistant Director of Agriculture", "phone": "9446606323", "email": "adakalamassery1@gmail.com"},
    {"district": "Ernakulam", "office": "Agricultural Officer Krishi Bhavan Tripunithura", "officer_name": "SONIA KP", "designation": "Agriculture Officer", "phone": "9495569941", "email": "krishibhavantripunithura@gmail.com"},
    # Thrissur
    {"district": "Thrissur", "office": "Agricultural Officer Krishi Bhavan Ollur Thrissur", "officer_name": "E.N.RAVINDRAN", "designation": "Agriculture Officer", "phone": "9383471327", "email": "ollurao@gmail.com"},
    {"district": "Thrissur", "office": "Agricultural Officer Krishi Bhavan Chalakudy / Melur", "officer_name": "RAHUL", "designation": "Agriculture Officer", "phone": "9383471376", "email": "aokbmeloor@gmail.com"},
    {"district": "Thrissur", "office": "Agricultural Officer Krishi Bhavan Kodakara Thrissur", "officer_name": "SWATHYLAKHSMI P V", "designation": "Agriculture Officer", "phone": "9383471198", "email": "aokodakara@gmail.com"},
    {"district": "Thrissur", "office": "Agricultural Officer Krishi Bhavan Wadakanchery Thrissur", "officer_name": "SMITHA M K", "designation": "Agriculture Officer", "phone": "9383471219", "email": "aowadakkanchery@gmail.com"},
    {"district": "Thrissur", "office": "Agricultural Officer Krishi Bhavan Kunnamkulam / Chowannur", "officer_name": "Sruthi", "designation": "Agriculture Officer", "phone": "9383471303", "email": "chowannurao@gmail.com"},
    # Palakkad
    {"district": "Palakkad", "office": "Agricultural Officer Krishi Bhavan Palakkad / Pirayiri", "officer_name": "Rasmi Krishnan", "designation": "Agriculture Officer", "phone": "9383471561", "email": "kbpirayiri@gmail.com"},
    {"district": "Palakkad", "office": "Agricultural Officer Krishi Bhavan Mannarkad / Karimba", "officer_name": "P.SAJIDALI", "designation": "Agriculture Officer", "phone": "9383471497", "email": "karimbakrishibhavan@gmail.com"},
    {"district": "Palakkad", "office": "Agricultural Officer Krishi Bhavan Ottappalam / Shornur", "officer_name": "BIJU P", "designation": "Agricultural Field Officer", "phone": "9383471513", "email": "kbshoranur@gmail.com"},
    {"district": "Palakkad", "office": "Agricultural Officer Krishi Bhavan Alathur Palakkad", "officer_name": "SRUTHY K", "designation": "Agriculture Officer", "phone": "9383471563", "email": "aoalathurkb@gmail.com"},
    {"district": "Palakkad", "office": "Agricultural Officer Krishi Bhavan Kollengode Palakkad", "officer_name": "Rahul Raj M", "designation": "Agriculture Officer", "phone": "9947231642", "email": "rahulrajm2013@gmail.com"},
    {"district": "Palakkad", "office": "Agricultural Officer Krishi Bhavan Chittur / Tathamangalam", "officer_name": "SAROJA", "designation": "Agricultural Field Officer", "phone": "9383471541", "email": "kbchturpkd.agri@kerala.gov.in"},
    {"district": "Palakkad", "office": "Agricultural Officer Krishi Bhavan Agali (Attappadi) Palakkad", "officer_name": "DEEPA", "designation": "Agriculture Officer", "phone": "9383471537", "email": "kbagali705@gmail.com"},
    # Malappuram
    {"district": "Malappuram", "office": "Agricultural Officer Krishi Bhavan Malappuram", "officer_name": "VINODKUMAR", "designation": "Agriculture Officer", "phone": "04832434673", "email": "afokbmpm@gmail.com"},
    {"district": "Malappuram", "office": "Agricultural Officer Krishi Bhavan Ponnani Malappuram", "officer_name": "SIVAPRASAD", "designation": "Agriculture Officer", "phone": "9383472145", "email": "kannurkrishibhavan@gmail.com"},
    {"district": "Malappuram", "office": "Agricultural Officer Krishi Bhavan Tirur Malappuram", "officer_name": "ABUBAKKER P B", "designation": "Agriculture Officer", "phone": "9383471664", "email": "kbtirur@gmail.com"},
    {"district": "Malappuram", "office": "Agricultural Officer Krishi Bhavan Kottakkal Malappuram", "officer_name": "VAISAKHAN.M V", "designation": "Agriculture Officer", "phone": "9383471706", "email": "kbkottakkal@gmail.com"},
    {"district": "Malappuram", "office": "Agricultural Officer Krishi Bhavan Perinthalmanna", "officer_name": "REJINA VASUDEVAN T", "designation": "Agriculture Officer", "phone": "9383471728", "email": "kbprnlmnmlp.agri@kerala.gov.in"},
    {"district": "Malappuram", "office": "Agricultural Officer Krishi Bhavan Manjeri Malappuram", "officer_name": "BINDHIYA", "designation": "Agriculture Officer", "phone": "9383471739", "email": "kbmnjrmlp.agri@kerala.gov.in"},
    {"district": "Malappuram", "office": "Agricultural Officer Krishi Bhavan Nilambur / Edakkara", "officer_name": "NEETHUTHANKAM C", "designation": "Agriculture Officer", "phone": "9383471762", "email": "edakkarakb@gmail.com"},
    # Kozhikode
    {"district": "Kozhikode", "office": "Agricultural Officer Krishi Bhavan Kozhikode City", "officer_name": "Mohammed Salim K T", "designation": "Agriculture Officer", "phone": "04952960048", "email": "afokozhikode@gmail.com"},
    {"district": "Kozhikode", "office": "Agricultural Officer Krishi Bhavan Vatakara Kozhikode", "officer_name": "abdurahiman", "designation": "Agriculture Officer", "phone": "9383471909", "email": "vatakarakbkzd@gmail.com"},
    {"district": "Kozhikode", "office": "Agricultural Officer Krishi Bhavan Koyilandy Kozhikode", "officer_name": "VIDYA P", "designation": "Assistant Director of Agriculture", "phone": "9383471885", "email": "adatuneri.agri@kerala.gov.in"},
    {"district": "Kozhikode", "office": "Agricultural Officer Krishi Bhavan Thamarassery Kozhikode", "officer_name": "MOIDEENSHA", "designation": "Agriculture Officer", "phone": "04952223828", "email": "thamarasserykbkzd@gmail.com"},
    {"district": "Kozhikode", "office": "Agricultural Officer Krishi Bhavan Balussery Kozhikode", "officer_name": "VIDYA", "designation": "Agriculture Officer", "phone": "9383471896", "email": "balusserykbkzd@gmail.com"},
    # Wayanad
    {"district": "Wayanad", "office": "Agricultural Officer Krishi Bhavan Kalppetta Wayanad", "officer_name": "AKHIL P", "designation": "Agriculture Officer", "phone": "9383471928", "email": "akhilayipoil7@gmail.com"},
    {"district": "Wayanad", "office": "Agricultural Officer Krishi Bhavan Sulthan Bathery", "officer_name": "AJIL", "designation": "Agriculture Officer", "phone": "9383471958", "email": "aokbsbi@gmail.com"},
    {"district": "Wayanad", "office": "Agricultural Officer Krishi Bhavan Mananthavadi Wayanad", "officer_name": "Sandra Maria", "designation": "Agriculture Officer", "phone": "9383471576", "email": "kbpulpally@gmail.com"},
    {"district": "Wayanad", "office": "Agricultural Officer Krishi Bhavan Pulppalli Wayanad", "officer_name": "ANU", "designation": "Agriculture Officer", "phone": "9383471952", "email": "kbpulpally@gmail.com"},
    {"district": "Wayanad", "office": "Agricultural Officer Krishi Bhavan Vythiri Wayanad", "officer_name": "SALINI", "designation": "Agriculture Officer", "phone": "9383471938", "email": "kbvythiri@gmail.com"},
    # Kannur
    {"district": "Kannur", "office": "Agricultural Officer Krishi Bhavan Thalasseri Kannur", "officer_name": "Krishnan P P", "designation": "Agriculture Officer", "phone": "9383472117", "email": "kbthalassery@gmail.com"},
    {"district": "Kannur", "office": "Agricultural Officer Krishi Bhavan Payyannur Kannur", "officer_name": "SHEENA K V", "designation": "Agriculture Officer", "phone": "9383472251", "email": "krishibhavanpnr@gmail.com"},
    {"district": "Kannur", "office": "Agricultural Officer Krishi Bhavan Thaliparamba Kannur", "officer_name": "SREESHMA K", "designation": "Agriculture Officer", "phone": "9383472066", "email": "aotaliparamba@gmail.com"},
    {"district": "Kannur", "office": "Agricultural Officer Krishi Bhavan Mattannur Kannur", "officer_name": "Jencymol Thomas", "designation": "Agriculture Officer", "phone": "9383472230", "email": "kbmattannur@gmail.com"},
    {"district": "Kannur", "office": "Agricultural Officer Krishi Bhavan Iritty / Peravoor", "officer_name": "DONA SCARIA", "designation": "Agriculture Officer", "phone": "9383472172", "email": "donascaria16@gmail.com"},
    # Kasaragod
    {"district": "Kasaragod", "office": "Agricultural Officer Krishi Bhavan Kasargod", "officer_name": "SREEJA M P", "designation": "Agriculture Officer", "phone": "9383472310", "email": "afokbksd@gmail.com"},
    {"district": "Kasaragod", "office": "Agricultural Officer Krishi Bhavan Kanhangad Kasargod", "officer_name": "S Remeshkumar", "designation": "Agricultural Field Officer", "phone": "9946446805", "email": "afovyttila@gmail.com"},
    {"district": "Kasaragod", "office": "Agricultural Officer Krishi Bhavan Nileshwar Kasargod", "officer_name": "SHIJO K A", "designation": "Agriculture Officer", "phone": "9383472334", "email": "kbnlswarksd.agri@kerala.gov.in"},
    {"district": "Kasaragod", "office": "Agricultural Officer Krishi Bhavan Manjeswar Kasargod", "officer_name": "Ramachandran", "designation": "Agriculture Officer", "phone": "9383472283", "email": "manjeshwarkb321@gmail.com"}
]

# Normalize Kerala officers schema
kerala_clean_list = []
for i, item in enumerate(kerala_officers_input, start=1):
    loc_name = item.get("office", "").replace("Agricultural Officer Krishi Bhavan", "").replace("Assistant Director of Agriculture (ADA)", "").replace("Agricultural Officer", "").replace(item.get("district", ""), "").strip()
    norm = {
        "id": f"KL-{item.get('district', 'GEN').upper()[:3]}-{i:04d}",
        "state": "Kerala",
        "district": item.get("district"),
        "block_or_taluk": loc_name or item.get("district"),
        "department": "Agriculture Development & Farmers Welfare Department",
        "designation": item.get("designation") or "Agriculture Officer",
        "name": item.get("officer_name") or "Agricultural Officer",
        "mobile": item.get("phone") or "",
        "landline": "",
        "email": item.get("email") or "",
        "source": "https://cmo.kerala.gov.in/office_display_level_en.php",
        "office_type": "Krishi Bhavan / ADA Office"
    }
    kerala_clean_list.append(norm)

# 3. WRITE ORGANIZED FILES

# Indexing helpers
def build_district_index(officers_list):
    idx = {}
    for off in officers_list:
        dist = off.get("district") or "Unknown"
        if dist not in idx:
            idx[dist] = []
        idx[dist].append(off)
    return idx

# File 1: Tamil Nadu Officers
tn_file = os.path.join(RAW_DATA_PATH, "tamil_nadu_officers.json")
with open(tn_file, "w", encoding="utf-8") as f:
    json.dump({
        "state": "Tamil Nadu",
        "total_records": len(tn_clean_list),
        "districts_covered": sorted(list(set(x["district"] for x in tn_clean_list))),
        "district_index": build_district_index(tn_clean_list),
        "officers": tn_clean_list
    }, f, indent=2, ensure_ascii=False)
print(f"✅ Written Tamil Nadu Directory: {tn_file} ({len(tn_clean_list)} records across {len(set(x['district'] for x in tn_clean_list))} districts)")

# File 2: Kerala Officers
kl_file = os.path.join(RAW_DATA_PATH, "kerala_officers.json")
with open(kl_file, "w", encoding="utf-8") as f:
    json.dump({
        "state": "Kerala",
        "total_records": len(kerala_clean_list),
        "districts_covered": sorted(list(set(x["district"] for x in kerala_clean_list))),
        "district_index": build_district_index(kerala_clean_list),
        "officers": kerala_clean_list
    }, f, indent=2, ensure_ascii=False)
print(f"✅ Written Kerala Directory: {kl_file} ({len(kerala_clean_list)} records across {len(set(x['district'] for x in kerala_clean_list))} districts)")

# File 3: Master Combined Directory (Organized State -> District -> Officers Index)
master_file = os.path.join(RAW_DATA_PATH, "all_officers_directory.json")
combined_all = tn_clean_list + kerala_clean_list
with open(master_file, "w", encoding="utf-8") as f:
    json.dump({
        "title": "National Cooperative & Agricultural Officer Verified Directory",
        "version": "2.0.0",
        "total_records": len(combined_all),
        "states_covered": ["Tamil Nadu", "Kerala"],
        "index_by_district": build_district_index(combined_all),
        "states": {
            "Tamil Nadu": {
                "record_count": len(tn_clean_list),
                "districts": sorted(list(set(x["district"] for x in tn_clean_list))),
                "district_index": build_district_index(tn_clean_list),
                "officers": tn_clean_list
            },
            "Kerala": {
                "record_count": len(kerala_clean_list),
                "districts": sorted(list(set(x["district"] for x in kerala_clean_list))),
                "district_index": build_district_index(kerala_clean_list),
                "officers": kerala_clean_list
            }
        },
        "officers": combined_all
    }, f, indent=2, ensure_ascii=False)
print(f"✅ Written Combined Master Directory: {master_file} ({len(combined_all)} total verified officers)")
