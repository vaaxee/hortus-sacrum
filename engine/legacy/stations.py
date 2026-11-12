# Source : Missale Romanum, ed. typica 1920 (archive.org: 000missaleromanum-1920), texte copié tel qu'imprimé.
import datetime as dt
D=dt.date;TD=dt.timedelta
E=D(2027,3,28)
def S(x): return 'Statio ad '+x
ST={D(2026,11,29):S('S. Mariam majorem'),D(2026,12,6):S('S. Crucem in Jerusalem'),D(2026,12,13):S('S. Petrum'),
D(2026,12,16):S('S. Mariam majorem'),D(2026,12,18):S('Ss. duodecim Apostolos'),D(2026,12,19):S('S. Petrum'),D(2026,12,20):S('Ss. duodecim Apostolos'),
D(2026,12,25):'Statio ad S. Mariam majorem ad Praesepe ; ad S. Anastasiam ; ad S. Mariam majorem',
D(2026,12,26):S('S. Stephanum in Cælio monte'),D(2026,12,27):S('S. Mariam majorem'),D(2026,12,28):S('S. Paulum'),
D(2027,1,1):S('S. Mariam trans Tiberim'),D(2027,1,6):S('S. Petrum')}
seq=[(-63,'S. Laurentium extra muros'),(-56,'S. Paulum'),(-49,'S. Petrum'),(-46,'S. Sabinam'),(-45,'S. Georgium'),(-44,'Ss. Joannem et Paulum'),(-43,'S. Tryphonem'),
(-42,'S. Joannem in Laterano'),(-41,'S. Petrum ad Vincula'),(-40,'S. Anastasiam'),(-39,'S. Mariam majorem'),(-38,'S. Laurentium in Panisperna'),(-37,'Ss. duodecim Apostolos'),(-36,'S. Petrum'),
(-35,'S. Mariam in Domnica'),(-34,'S. Clementem'),(-33,'S. Balbinam'),(-32,'S. Caeciliam'),(-31,'S. Mariam trans Tiberim'),(-30,'S. Vitalem'),(-29,'Ss. Marcellinum et Petrum'),
(-28,'S. Laurentium extra muros'),(-27,'S. Marcum'),(-26,'S. Pudentianam'),(-25,'S. Xystum'),(-24,'Ss. Cosmam et Damianum'),(-23,'S. Laurentium in Lucina'),(-22,'S. Susannam'),
(-21,'S. Crucem in Jerusalem'),(-20,'Ss. Quatuor Coronatos'),(-19,'S. Laurentium in Damaso'),(-18,'S. Paulum'),(-17,'Ss. Silvestrum et Martinum'),(-16,'S. Eusebium'),(-15,'S. Nicolaum in Carcere'),
(-14,'S. Petrum'),(-13,'S. Chrysogonum'),(-12,'S. Cyriacum'),(-11,'S. Marcellum'),(-10,'S. Apollinarem'),(-9,'S. Stephanum in Cælio monte'),(-8,'S. Joannem ante Portam Latinam'),
(-7,'S. Joannem in Laterano'),(-6,'S. Praxedem'),(-5,'S. Priscam'),(-4,'S. Mariam majorem'),(-3,'S. Joannem in Laterano'),(-2,'S. Crucem in Jerusalem'),(-1,'S. Joannem in Laterano'),
(0,'S. Mariam majorem'),(1,'S. Petrum'),(2,'S. Paulum'),(3,'S. Laurentium extra muros'),(4,'Ss. duodecim Apostolos'),(5,'S. Mariam ad Martyres'),(6,'S. Joannem in Laterano'),(7,'S. Pancratium'),
(36,'S. Mariam majorem'),(37,'S. Joannem in Laterano'),(38,'S. Petrum'),(39,'S. Petrum'),(48,'S. Joannem in Laterano'),
(49,'S. Petrum'),(50,'S. Petrum ad Vincula'),(51,'S. Anastasiam'),(52,'S. Mariam majorem'),(53,'S. Laurentium extra muros'),(54,'Ss. duodecim Apostolos'),(55,'S. Petrum')]
for o,c in seq: ST[E+TD(o)]=S(c)
ST[D(2027,4,25)]='Litaniæ majores : '+S('S. Petrum')
ST[D(2027,9,15)]=S('S. Mariam majorem');ST[D(2027,9,17)]=S('Ss. duodecim Apostolos');ST[D(2027,9,18)]=S('S. Petrum')
