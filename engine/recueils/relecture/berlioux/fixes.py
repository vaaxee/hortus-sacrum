import json,re
B='/tmp/claude-0/berl/'
e=json.load(open(B+'ent2.json'))
G=[('((','«'),('))','»'),('inpace','in pace'),('Requiescant m pacel','Requiescant in pace !'),('in pacel','in pace !')]
F={
1:[("pleuren' ","pleurent "),('prescrivalent','prescrivaient'),('laissaide','laissai de'),("j'avaiséchappé","j'avais échappé"),('Com- : mémoraison','Commémoraison'),("si 'ancienne","si ancienne")],
2:[('éterni assez','éternels, ni assez'),('PA D en plaçant','en plaçant'),('dontil','dont il'),('devien- dront','deviendront'),('i^^^N saint','UN saint'),('votre mour.','votre amour.'),('deviendra-telle','deviendra-t-elle')],
3:[('salutaire pen e.','salutaire pensée,'),(':uDAS Machabée','JUDAS Machabée'),('foi)et','foi et'),('inanimes','inanimés'),('catholilique','catholique')],
4:[('in ortuné','infortuné'),('convers rez','converserez'),('cœur,pour','cœur, pour')],
5:[("n'agitpas","n'agit pas"),('à teur fuite','à leur fuite')],
6:[('théolosiens','théologiens'),('UAND les enfants','QUAND les enfants'),('“ dutn recordaremur','dum recordaremur'),('— - Mais','— Mais')],
7:[('cui-\n\n— li- sants','cuisants'),('cui- — li- sants','cuisants'),("Pur- '.gatoire","Purgatoire"),('pauvre àme','pauvre âme'),("l'a- vait","l'avait"),('naitre','naître'),('ERSON, chancelier','GERSON, chancelier')],
8:[('durée ^^2 des','durée des'),("c'COUTEZ","ÉCOUTEZ"),('90 Quelles','2° Quelles')],
9:[('20 Impuissance','2° Impuissance')],
10:[('BPg\n\n',''),('bap- tême','baptême'),('constitu ent','constituent'),("reposent en\n\nRequiescant","reposent en paix !\n\nRequiescant")],
11:[('vient déne:\n\nsarmer','vient désarmer'),('Pur gatoire','Purgatoire'),('héroï- ques','héroïques'),('CieLsi','Ciel, si'),('bonheur,avec','bonheur, avec'),('vient déne: sarmer','vient désarmer'),('vient déne:  sarmer','vient désarmer')],
12:[('dar.s','dans'),('soulagerons,nousles','soulagerons, nous les'),('auz pieds','aux pieds'),('ar- racha','arracha'),('Miser eminimei','Miseremini mei'),('abî- mes','abîmes'),('aus - tère','austère'),('Ta ernacle','Tabernacle'),("quevousm''avez","que vous m'avez"),('fer- __. ventes','ferventes')],
13:[('que| ','que '),('unjour','un jour'),('1° DÉLAISSÉES PAR LEURS AMIS.','1° Délaissées par leurs amis.'),('2° DÉLAISSÉES PAR LEURS PARENTS','2° Délaissées par leurs parents.')],
14:[('NoUS crovons','Nous croyons'),("l'Eglise,'","l'Eglise,"),('tra- hissent','trahissent'),('1° Nous POUVONS LES SOULAGER.','1° Nous pouvons les soulager.'),('2° Nous DEVONS LES SOULAGER.','2° Nous devons les soulager.')],
15:[('Un pau- ^^vre','Un pauvre'),('transi ^5^42) de faim','transi de faim'),('frère? y> Quoi','frère? » Quoi'),("d'Infortude","d'infortune"),('HAGANUS,','CHAGANUS,')],
16:[('donnonsàDieu','donnons à Dieu'),('infidèles,^ [des','infidèles, des païens. »'),('félici- tent','félicitent'),('glorifie dieu','glorifie Dieu')],
17:[('cui-\n\n— li- sants','cuisants'),('m.orts','morts'),('disci- ples','disciples'),('écrile','écrite'),('ety fait','et y fait'),('terveur','ferveur'),('giâce','grâce'),('les âmes du purgatoire','les Ames du Purgatoire')],
18:[("se conter. !e pas d'encourager et (le ver et de consoler","se contente pas d'encourager et de consoler"),('Elle les DÉLIVRE. PREMIER POINT.','Elle les délivre.\n\nPREMIER POINT.'),("xx","se contente pas d'encourager et de consoler"),('les âmes du purgatoire','les Ames du Purgatoire')],
19:[('té- moignage','témoignage'),('eten offrant','et en offrant'),('cettte','cette'),('suisje','suis-je'),('Dans le purgatoire.','Dans le Purgatoire.'),('Dans le ciel.','Dans le Ciel.')],
20:[('maintennant','maintenant'),('comble de indifférence','comble de l\'indifférence'),('barbarie.Prierpour','barbarie. Prier pour'),('inévocations','invocations'),('so- yez-leur','soyez-leur'),('Ilus puissante','Plus puissante'),('montejusqu\'au','monte jusqu\'au'),('atttendent','attendent'),('UR le point de mourir','SUR le point de mourir')],
21:[('prières el en','prières et en'),('exercons','exerçons'),('nensée consolante','Pensée consolante'),('chrétiene','chrétienne'),('souffran ces','souffrances')],
22:[('2 Communion','2° Communion'),('aban- données','abandonnées')],
23:[('1° Il est offert par jésus-','1° Il est offert par Jésus-Christ.'),('tOUS les moyens','TOUS les moyens'),('res- sources','ressources'),('chétienne','chrétienne'),('me:ses','messes'),('^^E saint curé','LE saint curé')],
24:[('Purga- CA toire','Purgatoire'),('laProvidencenous','la Providence nous'),("l'esprit, “4 du","l'esprit, du")],
25:[('exem- plaire','exemplaire'),("l'en- seigne","l'enseigne"),('fidèl s','fidèles'),('jeunés','jeunes'),('p>.re','père'),('receviit','recevait'),('^on épouse','son épouse'),('chemin du ciel','chemin du Ciel')],
26:[('quise compose','qui se compose'),('saint ^5 François','saint François'),('pauves','pauvres')],
27:[('cui-\n\n— li- sants','cuisants'),('ins- tant','instant'),('mê- me','même'),('charitp','charité'),('inferaal','infernal'),('erains','crains')],
28:[('proue point.','PREMIER POINT.'),('^N raconte','ON raconte'),('obtendront','obtiendront'),('au purgatoire.','au Purgatoire.'),('les ames du purgatoire','les Ames du Purgatoire')],
29:[('misere- \n\nEXEMPLE','miseremini mei !\n\nEXEMPLE'),("l'appe- lait","l'appelait"),('2° POURQUOI LE PERMET-IL?','2° Pourquoi le permet-il ?'),('aux âmes du purgatoire','aux Ames du Purgatoire')],
30:[('promp-\n\nTEMENT.','promptement.'),('promp- \n\nTEMENT.','promptement.'),('promp- TEMENT.','promptement.'),('920 IL faut','2° Il faut'),('1° IL faut','1° Il faut'),('2° IL faut','2° Il faut'),('sû- res','sûres'),('déces','décès'),("l'àpropos","l'à-propos"),('àleurs','à leurs'),('T^N homme','UN homme'),('deux 4?^surtout','deux surtout'),('prolester','protester'),('opéra illorum','opera illorum')],
}
miss=[]
for x in e:
    n=int(x['cle'][2:]); t=x['corps']
    for a,b in G: t=t.replace(a,b)
    for a,b in F.get(n,[]):
        if a not in t: miss.append((n,a)); continue
        t=t.replace(a,b)
    t=re.sub(r'(?m)^[."]*\^+remier point','PREMIER POINT',t)
    t=re.sub(r'"?\^+remier point','PREMIER POINT',t)
    t=re.sub(r'[ \t]{2,}',' ',t)
    x['corps']=t
json.dump(e,open(B+'ent3.json','w'),ensure_ascii=False)
print('absents:',miss)
F2={
3:[('oS POINT.','PREMIER POINT.'),("qu'iL","qu'il"),("20 L'ENSEIGNEMENT de l'Eglise.","2° L'enseignement de l'Eglise.")],
4:[('Existence du Purgatoire (sue). 49\n\nTémoignage de notre raison. 2 Témoignage','Existence du Purgatoire (suite).\n\n1° Témoignage de notre raison. 2° Témoignage'),('Lys PREMIER POINT','PREMIER POINT'),('ce-- lui','celui'),('y jeune Ecossais','UN jeune Ecossais')],
12:[('NON —\n\n',''),('19 Elles nous sont unies par\n\nLES liens de la CHARITÉ.','1° Elles nous sont unies par les liens de la charité.'),('Crémier point. — « nez-vous, dit un pieux au-\n\n: teur, que','PREMIER POINT. — « Souvenez-vous, dit un pieux auteur, que'),('Dieu j rachetées','Dieu, rachetées'),("dE s'étant","s'étant"),("l''Eucharistie","l'Eucharistie"),('a Lout pouvoir','a tout pouvoir'),('PRIÈRE. |','PRIÈRE.')],
16:[('Ames DU Purgatoire','Ames du Purgatoire')],
18:[(". L'Amour de Marie.","L'Amour de Marie.")],
20:[('Crémier point.','PREMIER POINT.'),('il n pas de distance',"il n'y a pas de distance"),('acccueille','accueille'),('connaisnaissance','connaissance'),('mes. gémissements','mes gémissements'),('\n\nXj\n\nV','')],
25:[('pour\n\nLES morts.','pour les morts.')],
28:[('Pu gatoire','Purgatoire')],
}
miss=[]
for x in e:
    n=int(x['cle'][2:]); t=x['corps']
    for a,b in F2.get(n,[]):
        if a not in t: miss.append((n,a)); continue
        t=t.replace(a,b)
    t=re.sub(r"(?:(?<=^)|(?<=\n)|(?<=[.?!] ))(19|10|40|49|1»|4°|20|29|90|920|2)\s(?=[A-ZÉ])",lambda m:('1° ' if m.group(1)[0] in '14' else '2° '),t)
    t=re.sub(r"([.!?]) (Deuxième point\. —)",r"\1\n\n\2",t)
    x['corps']=t
json.dump(e,open(B+'ent3.json','w'),ensure_ascii=False)
print('absents2:',miss)
for x in e:
    for p in x['corps'].split('\n\n'):
        if len(p)<25 and p not in ('EXEMPLE.','PRIÈRE.','Requiescant in pace !'): print(x['cle'],repr(p))
F3={17:[("\n\nLES soulagions."," les soulagions."),("PREMIER POINT. - Considé-\n\n'^ rez","PREMIER POINT. — Considérez")],
18:[("Vierge\n\nMarie.","Vierge Marie.")],23:[("\n\nCHRIST.","")],27:[("L'acte e) héroïque","L'acte héroïque")],
15:[("\n\n(^t)(^t) ^^^\\^ @(^ ®(^t)","")]}
for x in e:
    n=int(x['cle'][2:]); t=x['corps']
    for a,b in F3.get(n,[]):
        if a not in t: print('absent3',n,repr(a)); continue
        t=t.replace(a,b)
    t=t.replace("PREMIER POINT.\n\n— ","PREMIER POINT. — ").replace("PRIÈRE. O\n\n","PRIÈRE.\n\nO ").replace("PRIÈRE. |","PRIÈRE.").replace("in pace!","in pace !")
    t=re.sub(r" \|(?=\n|$)","",t)
    if n==30: t=t.split("\n\nCONSEILS PRATIQUES")[0]
    ps=t.split('\n\n'); pre=[]
    for p in ps:
        if p.startswith('1°') or p.startswith('PREMIER'): break
        pre.append(p)
    x['corps']=t
    nom=x['titre'].split(' — ')[0]
    x['titre']=nom+(' — '+pre[-1].rstrip(' .:') if pre else '')
json.dump(e,open(B+'ent3.json','w'),ensure_ascii=False)
for x in e:
    print(x['cle'],x['titre'])
    for m in re.finditer(r".{0,30}[\^|<>{}\[\]@®©“”\"_~*#].{0,30}",x['corps']): print('   !!',repr(m.group(0)))
for x in e:
    t=x['corps']
    for a,b in [(' | ',' '),('Te” Sauveur','Le Sauveur'),('Judée,.^rencontra','Judée, rencontra'),('Catherine "2 de','Catherine de'),('divine. >','divine. »'),('miséricordes. >','miséricordes. »'),('L^horreur',"L'horreur")]:
        t=t.replace(a,b)
    x['corps']=t
json.dump(e,open(B+'ent3.json','w'),ensure_ascii=False)
