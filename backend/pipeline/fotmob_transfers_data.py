# -*- coding: utf-8 -*-
"""
Parses the user's comprehensive FotMob transfer list and applies every transfer to the DB.
"""
import os
import sys
import re
import sqlite3

RAW_TEXT = """
[CFR Cluj](https://www.fotmob.com/ko/teams/9731/overview/cfr-cluj)[Al-Wasl](https://www.fotmob.com/ko/teams/102111/overview/al-wasl)
[CBKurt Zouma](https://www.fotmob.com/ko/players/281207/kurt-zouma)
자유 이적
3월 3일
[Vasco da Gama](https://www.fotmob.com/ko/teams/10276/overview/vasco-da-gama)Free agent
[AMPhilippe Coutinho](https://www.fotmob.com/ko/players/184536/philippe-coutinho)
자유 이적
2월 21일
Free agent
[Feyenoord](https://www.fotmob.com/ko/teams/10235/overview/feyenoord)
[LWRaheem Sterling](https://www.fotmob.com/ko/players/246575/raheem-sterling)
자유 이적
2월 13일
Free agent
[Eibar](https://www.fotmob.com/ko/teams/8372/overview/eibar)
[RBJuan Bernat](https://www.fotmob.com/ko/players/282691/juan-bernat)
자유 이적
2월 13일
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)
[RBÁlex Jiménez](https://www.fotmob.com/ko/players/1526689/alex-jimenez)
€1850만
2월 12일
[Al Nassr FC](https://www.fotmob.com/ko/teams/101918/overview/al-nassr-fc)[Zenit](https://www.fotmob.com/ko/teams/8698/overview/zenit)
[STJhon Durán](https://www.fotmob.com/ko/players/1088066/jhon-duran)
€275만. 임대 중
2월 10일
[Rennes](https://www.fotmob.com/ko/teams/9851/overview/rennes)[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)
[CBJérémy Jacquet](https://www.fotmob.com/ko/players/1473534/jeremy-jacquet)
€6360만
2월 8일
[Wolves](https://www.fotmob.com/ko/teams/8602/overview/wolves)[Palmeiras](https://www.fotmob.com/ko/teams/10283/overview/palmeiras)
[LWJhon Arias](https://www.fotmob.com/ko/players/1023030/jhon-arias)
€2500만
2월 8일
[Torino](https://www.fotmob.com/ko/teams/9804/overview/torino)Free agent
[CBPerr Schuurs](https://www.fotmob.com/ko/players/726127/perr-schuurs)
2월 7일
[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)Free agent
[CMXaver Schlager](https://www.fotmob.com/ko/players/620027/xaver-schlager)
자유 이적
2월 6일
Free agent
[Pescara](https://www.fotmob.com/ko/teams/9878/overview/pescara)
[AMLorenzo Insigne](https://www.fotmob.com/ko/players/193441/lorenzo-insigne)
자유 이적
2월 6일
Free agent
[Fenerbahçe](https://www.fotmob.com/ko/teams/8695/overview/fenerbahce)
[DMN'Golo Kanté](https://www.fotmob.com/ko/players/319300/ngolo-kante)
자유 이적
2월 4일
Neom SC
[Al Hilal](https://www.fotmob.com/ko/teams/2529/overview/al-hilal)
[AMSaïmon Bouabré](https://www.fotmob.com/ko/players/1487959/saimon-bouabre)
€2300만
2월 4일
[Fenerbahçe](https://www.fotmob.com/ko/teams/8695/overview/fenerbahce)[Al Ittihad](https://www.fotmob.com/ko/teams/8577/overview/al-ittihad)
[STYoussef En-Nesyri](https://www.fotmob.com/ko/players/788555/youssef-en-nesyri)
€1500만
2월 4일
[Al Ittihad](https://www.fotmob.com/ko/teams/8577/overview/al-ittihad)Free agent
[DMN'Golo Kanté](https://www.fotmob.com/ko/players/319300/ngolo-kante)
자유 이적
2월 4일
[Monaco](https://www.fotmob.com/ko/teams/9829/overview/monaco)[Al Ittihad](https://www.fotmob.com/ko/teams/8577/overview/al-ittihad)
[STGeorge Ilenikhena](https://www.fotmob.com/ko/players/1431516/george-ilenikhena)
€3000만
2월 3일
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)
[CBAxel Disasi](https://www.fotmob.com/ko/players/696646/axel-disasi)
임대
2월 3일
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Everton](https://www.fotmob.com/ko/teams/8668/overview/everton)
[STTyrique George](https://www.fotmob.com/ko/players/1424875/tyrique-george)
임대
2월 3일
[Sunderland](https://www.fotmob.com/ko/teams/8472/overview/sunderland)[Monaco](https://www.fotmob.com/ko/teams/9829/overview/monaco)
[LWSimon Adingra](https://www.fotmob.com/ko/players/1227012/simon-adingra)
임대
2월 3일
[Al Ittihad](https://www.fotmob.com/ko/teams/8577/overview/al-ittihad)[Al Hilal](https://www.fotmob.com/ko/teams/2529/overview/al-hilal)
[STKarim Benzema](https://www.fotmob.com/ko/players/26166/karim-benzema)
€2500만
2월 3일
[Wolves](https://www.fotmob.com/ko/teams/8602/overview/wolves)[Crystal Palace](https://www.fotmob.com/ko/teams/9826/overview/crystal-palace)
[STJørgen Strand Larsen](https://www.fotmob.com/ko/players/821100/jorgen-strand-larsen)
€4970만
2월 3일
[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)[Sheff Utd](https://www.fotmob.com/ko/teams/8657/overview/sheff-utd)
[CMKalvin Phillips](https://www.fotmob.com/ko/players/609755/kalvin-phillips)
임대
2월 3일
[Atalanta](https://www.fotmob.com/ko/teams/8524/overview/atalanta)[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)
[STAdemola Lookman](https://www.fotmob.com/ko/players/690516/ademola-lookman)
€3500만
2월 3일
[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)
[RWBrajan Gruda](https://www.fotmob.com/ko/players/1430151/brajan-gruda)
임대
2월 2일
[Rennes](https://www.fotmob.com/ko/teams/9851/overview/rennes)[Al Hilal](https://www.fotmob.com/ko/teams/2529/overview/al-hilal)
[STMohamed Meïté](https://www.fotmob.com/ko/players/1693546/mohamed-meite)
€3000만
2월 2일
[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)[Ajax](https://www.fotmob.com/ko/teams/8593/overview/ajax)
[LBOleksandr Zinchenko](https://www.fotmob.com/ko/players/623621/oleksandr-zinchenko)
€150만
2월 2일
[Bologna](https://www.fotmob.com/ko/teams/9857/overview/bologna)[Paris FC](https://www.fotmob.com/ko/teams/6379/overview/paris-fc)
[STCiro Immobile](https://www.fotmob.com/ko/players/161660/ciro-immobile)
자유 이적
2월 2일
[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)[Crystal Palace](https://www.fotmob.com/ko/teams/9826/overview/crystal-palace)
[RWEvann Guessand](https://www.fotmob.com/ko/players/1087966/evann-guessand)
임대
1월 31일
[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)[Fulham](https://www.fotmob.com/ko/teams/9879/overview/fulham)
[RWOscar Bobb](https://www.fotmob.com/ko/players/1113790/oscar-bobb)
€3120만
1월 31일
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)Free agent
[LWRaheem Sterling](https://www.fotmob.com/ko/players/246575/raheem-sterling)
자유 이적
1월 30일
[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)[San Jose](https://www.fotmob.com/ko/teams/6603/overview/san-jose)
[LWTimo Werner](https://www.fotmob.com/ko/players/450980/timo-werner)
자유 이적
1월 30일
[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)[Flamengo](https://www.fotmob.com/ko/teams/9770/overview/flamengo)
[AMLucas Paquetá](https://www.fotmob.com/ko/players/766435/lucas-paqueta)
€4200만
1월 30일
[Wrexham](https://www.fotmob.com/ko/teams/9841/overview/wrexham)[Charlton](https://www.fotmob.com/ko/teams/8451/overview/charlton)
[CBConor Coady](https://www.fotmob.com/ko/players/247761/conor-coady)
임대
1월 30일
[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)[Burnley](https://www.fotmob.com/ko/teams/8191/overview/burnley)
[DMJames Ward-Prowse](https://www.fotmob.com/ko/players/279490/james-ward-prowse)
임대
1월 29일
[Juventus](https://www.fotmob.com/ko/teams/9885/overview/juventus)[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)
[DMDouglas Luiz](https://www.fotmob.com/ko/players/787350/douglas-luiz)
€200만. 임대 중
1월 29일
[Beşiktaş](https://www.fotmob.com/ko/teams/10188/overview/besiktas)[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)
[STTammy Abraham](https://www.fotmob.com/ko/players/749661/tammy-abraham)
€2100만
1월 28일
[Vasco da Gama](https://www.fotmob.com/ko/teams/10276/overview/vasco-da-gama)[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)
[RWRayan](https://www.fotmob.com/ko/players/1478295/rayan)
€2850만
1월 28일
[Roma](https://www.fotmob.com/ko/teams/8686/overview/roma)[Beşiktaş](https://www.fotmob.com/ko/teams/10188/overview/besiktas)
[STTammy Abraham](https://www.fotmob.com/ko/players/749661/tammy-abraham)
€1300만
1월 27일
[Hellas Verona](https://www.fotmob.com/ko/teams/9876/overview/hellas-verona)[Napoli](https://www.fotmob.com/ko/teams/9875/overview/napoli)
[STGiovane Nascimento](https://www.fotmob.com/ko/players/1355574/giovane-nascimento)
€2000만
1월 25일
[Napoli](https://www.fotmob.com/ko/teams/9875/overview/napoli)[Nottm Forest](https://www.fotmob.com/ko/teams/10203/overview/nottm-forest)
[STLorenzo Lucca](https://www.fotmob.com/ko/players/1212630/lorenzo-lucca)
€200만. 임대 중
1월 24일
[Napoli](https://www.fotmob.com/ko/teams/9875/overview/napoli)[Galatasaray](https://www.fotmob.com/ko/teams/8637/overview/galatasaray)
[LWNoa Lang](https://www.fotmob.com/ko/players/837341/noa-lang)
€200만. 임대 중
1월 24일
[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)[Marseille](https://www.fotmob.com/ko/teams/8592/overview/marseille)
[CMEthan Nwaneri](https://www.fotmob.com/ko/players/1254234/ethan-nwaneri)
임대
1월 23일
[Feyenoord](https://www.fotmob.com/ko/teams/10235/overview/feyenoord)[Marseille](https://www.fotmob.com/ko/teams/8592/overview/marseille)
[DMQuinten Timber](https://www.fotmob.com/ko/players/970563/quinten-timber)
€450만
1월 23일
[Barcelona](https://www.fotmob.com/ko/teams/8634/overview/barcelona)[Girona](https://www.fotmob.com/ko/teams/7732/overview/girona)
[골키퍼Marc-André ter Stegen](https://www.fotmob.com/ko/players/184554/marc-andre-ter-stegen)
임대
1월 21일
[Crystal Palace](https://www.fotmob.com/ko/teams/9826/overview/crystal-palace)[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)
[CBMarc Guéhi](https://www.fotmob.com/ko/players/844425/marc-guehi)
€2300만
1월 20일
[Leeds](https://www.fotmob.com/ko/teams/8463/overview/leeds)[Fiorentina](https://www.fotmob.com/ko/teams/8535/overview/fiorentina)
[RWJack Harrison](https://www.fotmob.com/ko/players/751649/jack-harrison)
€100만. 임대 중
1월 19일
[Salzburg](https://www.fotmob.com/ko/teams/10013/overview/salzburg)[Le Havre](https://www.fotmob.com/ko/teams/9746/overview/le-havre)
[DMLucas Gourna-Douath](https://www.fotmob.com/ko/players/1137106/lucas-gourna-douath)
임대
1월 17일
[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)[Roma](https://www.fotmob.com/ko/teams/8686/overview/roma)
[STDonyell Malen](https://www.fotmob.com/ko/players/660301/donyell-malen)
€200만. 임대 중
1월 16일
[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)[Atalanta](https://www.fotmob.com/ko/teams/8524/overview/atletico-madrid)
[AMGiacomo Raspadori](https://www.fotmob.com/ko/players/951743/giacomo-raspadori)
€2200만
1월 16일
[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)[Leeds](https://www.fotmob.com/ko/teams/8463/overview/leeds)
[AMFacundo Buonanotte](https://www.fotmob.com/ko/players/1336566/facundo-buonanotte)
임대
1월 16일
[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)[Auxerre](https://www.fotmob.com/ko/teams/8583/overview/auxerre)
[RWRomain Faivre](https://www.fotmob.com/ko/players/904021/romain-faivre)
임대
1월 16일
[Marseille](https://www.fotmob.com/ko/teams/8592/overview/marseille)[Roma](https://www.fotmob.com/ko/teams/8686/overview/roma)
[STRobinio Vaz](https://www.fotmob.com/ko/players/1705134/robinio-vaz)
€2200만
1월 15일
[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)[Tottenham](https://www.fotmob.com/ko/teams/8586/overview/tottenham)
[CMConor Gallagher](https://www.fotmob.com/ko/players/966027/conor-gallagher)
€4000만
1월 15일
[Leicester](https://www.fotmob.com/ko/teams/8197/overview/leicester)[Monaco](https://www.fotmob.com/ko/teams/9829/overview/monaco)
[CBWout Faes](https://www.fotmob.com/ko/players/693678/wout-faes)
임대
1월 14일
[Al Hilal](https://www.fotmob.com/ko/teams/2529/overview/al-hilal)[Barcelona](https://www.fotmob.com/ko/teams/8634/overview/barcelona)
[LBJoão Cancelo](https://www.fotmob.com/ko/players/361757/joao-cancelo)
€400만. 임대 중
1월 13일
[Panathinaikos](https://www.fotmob.com/ko/teams/10200/overview/panathinaikos)[Gremio](https://www.fotmob.com/ko/teams/9769/overview/gremio)
[RWTetê](https://www.fotmob.com/ko/players/1039534/tete)
밝혀지지 않음
1월 12일
[Zenit](https://www.fotmob.com/ko/teams/8698/overview/zenit)[Cruzeiro](https://www.fotmob.com/ko/teams/9781/overview/cruzeiro)
[DMGérson](https://www.fotmob.com/ko/players/580604/gerson)
€2700만
1월 11일
[Ajax](https://www.fotmob.com/ko/teams/8593/overview/ajax)[Lazio](https://www.fotmob.com/ko/teams/8543/overview/lazio)
[CMKenneth Taylor](https://www.fotmob.com/ko/players/970565/kenneth-taylor)
€1685만
1월 10일
[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)
[RWAntoine Semenyo](https://www.fotmob.com/ko/players/933576/antoine-semenyo)
€7200만
1월 9일
[Lazio](https://www.fotmob.com/ko/teams/8543/overview/lazio)[Fenerbahçe](https://www.fotmob.com/ko/teams/8695/overview/fenerbahce)
[DMMattéo Guendouzi](https://www.fotmob.com/ko/players/800609/matteo-guendouzi)
€2800만
1월 9일
[Nottm Forest](https://www.fotmob.com/ko/teams/10203/overview/nottm-forest)[Frankfurt](https://www.fotmob.com/ko/teams/9810/overview/frankfurt)
[STArnaud Kalimuendo-Muinga](https://www.fotmob.com/ko/players/1095445/arnaud-kalimuendo-muinga)
€150만. 임대 중
1월 8일
[Lazio](https://www.fotmob.com/ko/teams/8543/overview/lazio)[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)
[STValentín Castellanos](https://www.fotmob.com/ko/players/823658/valentin-castellanos)
€2900만
1월 5일
[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)[Sporting CP](https://www.fotmob.com/ko/teams/9768/overview/sporting-cp)
[LWLuis Guilherme](https://www.fotmob.com/ko/players/1458757/luis-guilherme)
€1400만
1월 5일
[Cruzeiro](https://www.fotmob.com/ko/teams/9781/overview/cruzeiro)[Santos FC](https://www.fotmob.com/ko/teams/8514/overview/santos-fc)
[STGabriel Barbosa](https://www.fotmob.com/ko/players/450848/gabriel-barbosa)
임대
1월 4일
[Gil Vicente](https://www.fotmob.com/ko/teams/9764/overview/gil-vicente)[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)
[STPablo](https://www.fotmob.com/ko/players/1227326/pablo)
€2300만
1월 3일
[Tottenham](https://www.fotmob.com/ko/teams/8586/overview/tottenham)[Crystal Palace](https://www.fotmob.com/ko/teams/9826/overview/crystal-palace)
[RWBrennan Johnson](https://www.fotmob.com/ko/players/1076756/brennan-johnson)
€4000만
1월 3일
[Frankfurt](https://www.fotmob.com/ko/teams/9810/overview/frankfurt)[Nice](https://www.fotmob.com/ko/teams/9831/overview/nice)
[STElye Wahi](https://www.fotmob.com/ko/players/1213430/elye-wahi)
임대
1월 2일
Free agent
[Atletico MG](https://www.fotmob.com/ko/teams/10272/overview/atletico-mg)
[LBRenan Lodi](https://www.fotmob.com/ko/players/793876/renan-lodi)
자유 이적
2025. 12. 28.
[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)[Lens](https://www.fotmob.com/ko/teams/8588/overview/lens)
[DMAmadou Haidara](https://www.fotmob.com/ko/players/688830/amadou-haidara)
€200만
2025. 12. 24.
[Real Madrid](https://www.fotmob.com/ko/teams/8633/overview/real-madrid)[Lyon](https://www.fotmob.com/ko/teams/9748/overview/lyon)
[RWEndrick](https://www.fotmob.com/ko/players/1406729/endrick)
임대
2025. 12. 24.
Free agent
[Ajax](https://www.fotmob.com/ko/teams/8593/overview/ajax)
[CBTakehiro Tomiyasu](https://www.fotmob.com/ko/players/664444/takehiro-tomiyasu)
자유 이적
2025. 12. 17.
Free agent
[Inter Miami CF](https://www.fotmob.com/ko/teams/960720/overview/inter-miami-cf)
[LBSergio Reguilón](https://www.fotmob.com/ko/players/724436/sergio-reguilon)
자유 이적
2025. 12. 16.
[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)[Inter Miami CF](https://www.fotmob.com/ko/teams/960720/overview/inter-miami-cf)
[CMRodrigo De Paul](https://www.fotmob.com/ko/players/324578/rodrigo-de-paul)
€1500만
2025. 12. 12.
Free agent
[Wydad Casablanca](https://www.fotmob.com/ko/teams/102050/overview/wydad-casablanca)
[RWHakim Ziyech](https://www.fotmob.com/ko/players/360559/hakim-ziyech)
자유 이적
2025. 10. 25.
[Al Hilal](https://www.fotmob.com/ko/teams/2529/overview/al-hilal)Free agent
[LBRenan Lodi](https://www.fotmob.com/ko/players/793876/renan-lodi)
자유 이적
2025. 9. 14.
[AEK Athens](https://www.fotmob.com/ko/teams/8563/overview/aek-athens)[Monterrey](https://www.fotmob.com/ko/teams/7849/overview/monterrey)
[STAnthony Martial](https://www.fotmob.com/ko/players/413557/anthony-martial)
€383만
2025. 9. 13.
[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)[Trabzonspor](https://www.fotmob.com/ko/teams/9752/overview/trabzonspor)
[골키퍼André Onana](https://www.fotmob.com/ko/players/611491/andre-onana)
임대
2025. 9. 12.
[Al Nassr FC](https://www.fotmob.com/ko/teams/101918/overview/al-nassr-fc)[Athletic Club](https://www.fotmob.com/ko/teams/8315/overview/athletic-club)
[CBAymeric Laporte](https://www.fotmob.com/ko/players/411617/aymeric-laporte)
€1000만
2025. 9. 12.
[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)[Al-Taawoun](https://www.fotmob.com/ko/teams/205686/overview/al-taawoun)
[RWRomain Faivre](https://www.fotmob.com/ko/players/904021/romain-faivre)
임대
2025. 9. 11.
Free agent
[Wolfsburg](https://www.fotmob.com/ko/teams/8721/overview/wolfsburg)
[CMChristian Eriksen](https://www.fotmob.com/ko/players/157723/christian-eriksen)
자유 이적
2025. 9. 11.
[Bahia](https://www.fotmob.com/ko/teams/7877/overview/bahia)Neom SC
[STLuciano Rodríguez](https://www.fotmob.com/ko/players/1285291/luciano-rodriguez)
€2000만
2025. 9. 11.
[PSG](https://www.fotmob.com/ko/teams/9847/overview/psg)Qatar SC
[CBPresnel Kimpembe](https://www.fotmob.com/ko/players/562035/presnel-kimpembe)
밝혀지지 않음
2025. 9. 8.
[Reims](https://www.fotmob.com/ko/teams/9837/overview/reims)[Al Ahli](https://www.fotmob.com/ko/teams/2530/overview/al-ahli)
[DMValentin Atangana Edoa](https://www.fotmob.com/ko/players/1439625/valentin-atangana-edoa)
€2500만
2025. 9. 7.
[Braga](https://www.fotmob.com/ko/teams/10264/overview/braga)[Al Ittihad](https://www.fotmob.com/ko/teams/8577/overview/al-ittihad)
[LWRoger Fernandes](https://www.fotmob.com/ko/players/1283094/roger-fernandes)
€3200만
2025. 9. 6.
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Dinamo Zagreb](https://www.fotmob.com/ko/teams/10156/overview/dinamo-zagreb)
[DMIsmaël Bennacer](https://www.fotmob.com/ko/players/609624/ismael-bennacer)
임대
2025. 9. 5.
[Al Hilal](https://www.fotmob.com/ko/teams/2529/overview/al-hilal)[Al-Rayyan](https://www.fotmob.com/ko/teams/101898/overview/al-rayyan)
[STAleksandar Mitrovic](https://www.fotmob.com/ko/players/351860/aleksandar-mitrovic)
자유 이적
2025. 9. 4.
[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)[CFR Cluj](https://www.fotmob.com/ko/teams/9731/overview/cfr-cluj)
[CBKurt Zouma](https://www.fotmob.com/ko/players/281207/kurt-zouma)
자유 이적
2025. 9. 4.
[FK Crvena Zvezda](https://www.fotmob.com/ko/teams/8687/overview/fk-crvena-zvezda)[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)
[CBVeljko Milosavljevic](https://www.fotmob.com/ko/players/1666977/veljko-milosavljevic)
€1500만
2025. 9. 3.
[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)[Galatasaray](https://www.fotmob.com/ko/teams/8637/overview/galatasaray)
[DMIlkay Gündogan](https://www.fotmob.com/ko/players/178818/ilkay-gundogan)
자유 이적
2025. 9. 3.
[Benfica](https://www.fotmob.com/ko/teams/9772/overview/benfica)[Burnley](https://www.fotmob.com/ko/teams/8191/overview/burnley)
[CMFlorentino](https://www.fotmob.com/ko/players/793255/florentino)
€200만. 임대 중
2025. 9. 3.
[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)[FC Porto](https://www.fotmob.com/ko/teams/9773/overview/fc-porto)
[CBJakub Kiwior](https://www.fotmob.com/ko/players/1021834/jakub-kiwior)
€200만. 임대 중
2025. 9. 3.
[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)[Fenerbahçe](https://www.fotmob.com/ko/teams/8695/overview/fenerbahce)
[골키퍼Ederson](https://www.fotmob.com/ko/players/363364/ederson)
€1100만
2025. 9. 2.
[Royal Antwerp](https://www.fotmob.com/ko/teams/9988/overview/royal-antwerp)[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)
[골키퍼Senne Lammens](https://www.fotmob.com/ko/players/1178602/senne-lammens)
€2100만
2025. 9. 2.
[PSG](https://www.fotmob.com/ko/teams/9847/overview/psg)[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)
[골키퍼Gianluigi Donnarumma](https://www.fotmob.com/ko/players/618878/gianluigi-donnarumma)
€3000만
2025. 9. 2.
[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)[Marseille](https://www.fotmob.com/ko/teams/8592/overview/marseille)
[DMMatthew O'Riley](https://www.fotmob.com/ko/players/866686/matthew-oriley)
€200만. 임대 중
2025. 9. 2.
[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)[Marseille](https://www.fotmob.com/ko/teams/8592/overview/marseille)
[CBNayef Aguerd](https://www.fotmob.com/ko/players/617310/nayef-aguerd)
€2300만
2025. 9. 2.
[Monaco](https://www.fotmob.com/ko/teams/9829/overview/monaco)[Rennes](https://www.fotmob.com/ko/teams/9851/overview/rennes)
[STBreel Embolo](https://www.fotmob.com/ko/players/527103/breel-embolo)
€1300만
2025. 9. 2.
[Como](https://www.fotmob.com/ko/teams/10171/overview/como)Free agent
[AMDele Alli](https://www.fotmob.com/ko/players/363333/dele-alli)
2025. 9. 2.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Strasbourg](https://www.fotmob.com/ko/teams/9848/overview/strasbourg)
[LBBen Chilwell](https://www.fotmob.com/ko/players/672469/ben-chilwell)
자유 이적
2025. 9. 2.
[Athletic Club](https://www.fotmob.com/ko/teams/8315/overview/athletic-club)[Levante](https://www.fotmob.com/ko/teams/8581/overview/levante)
[CMUnai Vencedor](https://www.fotmob.com/ko/players/1007717/unai-vencedor)
임대
2025. 9. 2.
[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)[Genoa](https://www.fotmob.com/ko/teams/10233/overview/genoa)
[RWMaxwel Cornet](https://www.fotmob.com/ko/players/426880/maxwel-cornet)
임대
2025. 9. 2.
[Trabzonspor](https://www.fotmob.com/ko/teams/9752/overview/trabzonspor)[Galatasaray](https://www.fotmob.com/ko/teams/8637/overview/galatasaray)
[골키퍼Ugurcan Çakir](https://www.fotmob.com/ko/players/603669/ugurcan-cakir)
€3300만
2025. 9. 2.
[Inter](https://www.fotmob.com/ko/teams/8636/overview/inter)[Marseille](https://www.fotmob.com/ko/teams/8592/overview/marseille)
[CBBenjamin Pavard](https://www.fotmob.com/ko/players/611223/benjamin-pavard)
€250만. 임대 중
2025. 9. 2.
Free agent
[Sevilla](https://www.fotmob.com/ko/teams/8302/overview/sevilla)
[STAlexis Sánchez](https://www.fotmob.com/ko/players/50047/alexis-sanchez)
자유 이적
2025. 9. 2.
[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)[Nottm Forest](https://www.fotmob.com/ko/teams/10203/overview/nottm-forest)
[LBOleksandr Zinchenko](https://www.fotmob.com/ko/players/623621/oleksandr-zinchenko)
임대
2025. 9. 2.
[Brentford](https://www.fotmob.com/ko/teams/9937/overview/brentford)[Newcastle](https://www.fotmob.com/ko/teams/10261/overview/newcastle)
[STYoane Wissa](https://www.fotmob.com/ko/players/666857/yoane-wissa)
€6500만
2025. 9. 2.
[Strasbourg](https://www.fotmob.com/ko/teams/9848/overview/strasbourg)[Nottm Forest](https://www.fotmob.com/ko/teams/10203/overview/nottm-forest)
[RWDilane Bakwa](https://www.fotmob.com/ko/players/1079539/dilane-bakwa)
€3500만
2025. 9. 2.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Bayern München](https://www.fotmob.com/ko/teams/9823/overview/bayern-munchen)
[STNicolas Jackson](https://www.fotmob.com/ko/players/1197347/nicolas-jackson)
€1650만. 임대 중
2025. 9. 2.
[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)
[AMHarvey Elliott](https://www.fotmob.com/ko/players/963964/harvey-elliott)
임대
2025. 9. 2.
[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)
[RWJadon Sancho](https://www.fotmob.com/ko/players/846381/jadon-sancho)
임대
2025. 9. 2.
[Ajax](https://www.fotmob.com/ko/teams/8593/overview/ajax)[Sunderland](https://www.fotmob.com/ko/teams/8472/overview/sunderland)
[STBrian Brobbey](https://www.fotmob.com/ko/players/940446/brian-brobbey)
€2000만
2025. 9. 2.
[Sevilla](https://www.fotmob.com/ko/teams/8302/overview/sevilla)[Benfica](https://www.fotmob.com/ko/teams/9772/overview/benfica)
[RWDodi Lukébakio](https://www.fotmob.com/ko/players/688876/dodi-lukebakio)
€2000만
2025. 9. 2.
[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)[Juventus](https://www.fotmob.com/ko/teams/9885/overview/juventus)
[STLoïs Openda](https://www.fotmob.com/ko/players/747767/lois-openda)
€330만. 임대 중
2025. 9. 2.
[Shakhtar Donetsk](https://www.fotmob.com/ko/teams/9728/overview/shakhtar-donetsk)[Fulham](https://www.fotmob.com/ko/teams/9879/overview/fulham)
[LWKevin](https://www.fotmob.com/ko/players/1318400/kevin)
€4000만
2025. 9. 2.
[Newcastle](https://www.fotmob.com/ko/teams/10261/overview/newcastle)[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)
[STAlexander Isak](https://www.fotmob.com/ko/players/690107/alexander-isak)
€1.4억
2025. 9. 2.
[Sporting CP](https://www.fotmob.com/ko/teams/9768/overview/sporting-cp)[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)
[STConrad Harder](https://www.fotmob.com/ko/players/1482294/conrad-harder)
€2410만
2025. 9. 2.
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Fulham](https://www.fotmob.com/ko/teams/9879/overview/fulham)
[LWSamuel Chukwueze](https://www.fotmob.com/ko/players/688300/samuel-chukwueze)
임대
2025. 9. 2.
[Como](https://www.fotmob.com/ko/teams/10171/overview/como)[Cagliari](https://www.fotmob.com/ko/teams/8529/overview/cagliari)
[STAndrea Belotti](https://www.fotmob.com/ko/players/309726/andrea-belotti)
2025. 9. 2.
[PSG](https://www.fotmob.com/ko/teams/9847/overview/psg)[Tottenham](https://www.fotmob.com/ko/teams/8586/overview/tottenham)
[STRandal Kolo Muani](https://www.fotmob.com/ko/players/823825/randal-kolo-muani)
임대
2025. 9. 2.
[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)[Inter](https://www.fotmob.com/ko/teams/8636/overview/inter)
[CBManuel Akanji](https://www.fotmob.com/ko/players/521318/manuel-akanji)
€100만. 임대 중
2025. 9. 2.
[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)[Sunderland](https://www.fotmob.com/ko/teams/8472/overview/sunderland)
[RBLutsharel Geertruida](https://www.fotmob.com/ko/players/881640/lutsharel-geertruida)
임대
2025. 9. 2.
[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)
[LBPiero Hincapié](https://www.fotmob.com/ko/players/1137667/piero-hincapie)
임대
2025. 9. 2.
[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)[Napoli](https://www.fotmob.com/ko/teams/9875/overview/napoli)
[STRasmus Højlund](https://www.fotmob.com/ko/players/1199272/rasmus-hojlund)
€600만. 임대 중
2025. 9. 2.
[Udinese](https://www.fotmob.com/ko/teams/8600/overview/udinese)Free agent
[STAlexis Sánchez](https://www.fotmob.com/ko/players/50047/alexis-sanchez)
자유 이적
2025. 9. 2.
[Villarreal](https://www.fotmob.com/ko/teams/10205/overview/villarreal)[Levante](https://www.fotmob.com/ko/teams/8581/overview/levante)
[STEtta Eyong](https://www.fotmob.com/ko/players/1392779/etta-eyong)
€300만
2025. 9. 2.
[PSG](https://www.fotmob.com/ko/teams/9847/overview/psg)[Fenerbahçe](https://www.fotmob.com/ko/teams/8695/overview/fenerbahce)
[AMMarco Asensio](https://www.fotmob.com/ko/players/498033/marco-asensio)
€750만
2025. 9. 2.
[Fenerbahçe](https://www.fotmob.com/ko/teams/8695/overview/fenerbahce)[Al Hilal](https://www.fotmob.com/ko/teams/2529/overview/al-hilal)
[CBYusuf Akçiçek](https://www.fotmob.com/ko/players/1561568/yusuf-akcicek)
€2500만
2025. 9. 2.
[PSG](https://www.fotmob.com/ko/teams/9847/overview/psg)[Real Sociedad](https://www.fotmob.com/ko/teams/8560/overview/real-sociedad)
[AMCarlos Soler](https://www.fotmob.com/ko/players/708890/carlos-soler)
€600만
2025. 9. 2.
[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)[Real Betis](https://www.fotmob.com/ko/teams/8603/overview/real-betis)
[RWAntony](https://www.fotmob.com/ko/players/967622/antony)
€2200만
2025. 9. 2.
[Toulouse](https://www.fotmob.com/ko/teams/9941/overview/toulouse)[Crystal Palace](https://www.fotmob.com/ko/teams/9826/overview/crystal-palace)
[CBJaydee Canvot](https://www.fotmob.com/ko/players/1664722/jaydee-canvot)
€2300만
2025. 9. 2.
[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)[Werder Bremen](https://www.fotmob.com/ko/teams/8697/overview/werder-bremen)
[STVictor Okoh Boniface](https://www.fotmob.com/ko/players/1035208/victor-okoh-boniface)
임대
2025. 9. 2.
[Marseille](https://www.fotmob.com/ko/teams/8592/overview/marseille)[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)
[CMAdrien Rabiot](https://www.fotmob.com/ko/players/352879/adrien-rabiot)
€900만
2025. 9. 2.
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Atalanta](https://www.fotmob.com/ko/teams/8524/overview/atalanta)
[DMYunus Musah](https://www.fotmob.com/ko/players/1137272/yunus-musah)
€400만. 임대 중
2025. 9. 2.
[Lyon](https://www.fotmob.com/ko/teams/9748/overview/lyon)[Villarreal](https://www.fotmob.com/ko/teams/10205/overview/villarreal)
[STGeorges Mikautadze](https://www.fotmob.com/ko/players/1117069/georges-mikautadze)
€3100만
2025. 9. 2.
Free agent
[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)
[CBVictor Nilsson Lindelöf](https://www.fotmob.com/ko/players/258269/victor-nilsson-lindelof)
자유 이적
2025. 9. 2.
[Leicester](https://www.fotmob.com/ko/teams/8197/overview/leicester)[VfB Stuttgart](https://www.fotmob.com/ko/teams/10269/overview/vfb-stuttgart)
[AMBilal El Khannouss](https://www.fotmob.com/ko/players/1340895/bilal-el-khannouss)
임대
2025. 9. 2.
Al Qadasiya
[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)
[DMEqui Fernández](https://www.fotmob.com/ko/players/1199959/equi-fernandez)
€2500만
2025. 9. 2.
[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)
[AMFacundo Buonanotte](https://www.fotmob.com/ko/players/1336566/facundo-buonanotte)
임대
2025. 9. 2.
[Panathinaikos](https://www.fotmob.com/ko/teams/10200/overview/panathinaikos)[Sporting CP](https://www.fotmob.com/ko/teams/9768/overview/sporting-cp)
[STFotis Ioannidis](https://www.fotmob.com/ko/players/899701/fotis-ioannidis)
€2200만
2025. 9. 1.
[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)[Napoli](https://www.fotmob.com/ko/teams/9875/overview/napoli)
[AMEljif Elmas](https://www.fotmob.com/ko/players/741049/eljif-elmas)
€200만. 임대 중
2025. 9. 1.
[Genk](https://www.fotmob.com/ko/teams/9987/overview/genk)[Wolves](https://www.fotmob.com/ko/teams/8602/overview/wolves)
[STTolu Arokodare](https://www.fotmob.com/ko/players/1072864/tolu-arokodare)
€2800만
2025. 9. 1.
[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)[Strasbourg](https://www.fotmob.com/ko/teams/9848/overview/strasbourg)
[AMJulio Enciso](https://www.fotmob.com/ko/players/1073742/julio-enciso)
€1850만
2025. 9. 1.
[Benfica](https://www.fotmob.com/ko/teams/9772/overview/benfica)[Fenerbahçe](https://www.fotmob.com/ko/teams/8695/overview/fenerbahce)
[LWKerem Aktürkoglu](https://www.fotmob.com/ko/players/1117570/kerem-akturkoglu)
€2250만
2025. 9. 1.
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)
[RBÁlex Jiménez](https://www.fotmob.com/ko/players/1526689/alex-jimenez)
임대
2025. 9. 1.
[Monaco](https://www.fotmob.com/ko/teams/9829/overview/monaco)[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)
[AMEliesse Ben Seghir](https://www.fotmob.com/ko/players/1393439/eliesse-ben-seghir)
€3200만
2025. 9. 1.
[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)[Marseille](https://www.fotmob.com/ko/teams/8592/overview/marseille)
[DMArthur Vermeeren](https://www.fotmob.com/ko/players/1387389/arthur-vermeeren)
€300만. 임대 중
2025. 8. 31.
[Shakhtar Donetsk](https://www.fotmob.com/ko/teams/9728/overview/shakhtar-donetsk)[Benfica](https://www.fotmob.com/ko/teams/9772/overview/benfica)
[AMGeorgiy Sudakov](https://www.fotmob.com/ko/players/1192398/georgiy-sudakov)
€675만. 임대 중
2025. 8. 31.
[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)
[LWAlejandro Garnacho](https://www.fotmob.com/ko/players/1203665/alejandro-garnacho)
€4500만
2025. 8. 31.
[VfB Stuttgart](https://www.fotmob.com/ko/teams/10269/overview/vfb-stuttgart)[Newcastle](https://www.fotmob.com/ko/teams/10261/overview/newcastle)
[STNick Woltemade](https://www.fotmob.com/ko/players/1106563/nick-woltemade)
€8500만
2025. 8. 31.
[Juventus](https://www.fotmob.com/ko/teams/9885/overview/juventus)[Nottm Forest](https://www.fotmob.com/ko/teams/10203/overview/nottm-forest)
[RBNicolò Savona](https://www.fotmob.com/ko/players/1622290/nicolo-savona)
€1500만
2025. 8. 30.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)
[STChristopher Nkunku](https://www.fotmob.com/ko/players/704523/christopher-nkunku)
€3500만
2025. 8. 30.
[Nordsjælland](https://www.fotmob.com/ko/teams/10202/overview/nordsjaelland)[Ipswich](https://www.fotmob.com/ko/teams/9902/overview/ipswich)
[RWSindre Walle Egeli](https://www.fotmob.com/ko/players/1307961/sindre-walle-egeli)
€2000만
2025. 8. 30.
[Villarreal](https://www.fotmob.com/ko/teams/10205/overview/villarreal)[Crystal Palace](https://www.fotmob.com/ko/teams/9826/overview/crystal-palace)
[AMYéremi Pino](https://www.fotmob.com/ko/players/1047676/yeremi-pino)
€3000만
2025. 8. 30.
[Wolves](https://www.fotmob.com/ko/teams/8602/overview/wolves)[Dortmund](https://www.fotmob.com/ko/teams/9789/overview/dortmund)
[STFábio Silva](https://www.fotmob.com/ko/players/1050158/fabio-silva)
€2260만
2025. 8. 30.
[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)[Tottenham](https://www.fotmob.com/ko/teams/8586/overview/tottenham)
[AMXavi Simons](https://www.fotmob.com/ko/players/1173787/xavi-simons)
€6000만
2025. 8. 30.
[Southampton](https://www.fotmob.com/ko/teams/8466/overview/southampton)[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)
[CMMateus Fernandes](https://www.fotmob.com/ko/players/1356312/mateus-fernandes)
€4400만
2025. 8. 29.
[Tottenham](https://www.fotmob.com/ko/teams/8586/overview/tottenham)[Hamburger SV](https://www.fotmob.com/ko/teams/9790/overview/hamburger-sv)
[CBLuka Vuskovic](https://www.fotmob.com/ko/players/1413996/luka-vuskovic)
임대
2025. 8. 29.
[Monaco](https://www.fotmob.com/ko/teams/9829/overview/monaco)[Galatasaray](https://www.fotmob.com/ko/teams/8637/overview/galatasaray)
[CBWilfried Singo](https://www.fotmob.com/ko/players/1027472/wilfried-singo)
€3000만
2025. 8. 28.
[Girona](https://www.fotmob.com/ko/teams/7732/overview/girona)[Wolves](https://www.fotmob.com/ko/teams/8602/overview/wolves)
[CBLadislav Krejcí](https://www.fotmob.com/ko/players/798029/ladislav-krejci)
임대
2025. 8. 28.
[Newcastle](https://www.fotmob.com/ko/teams/10261/overview/newcastle)[Middlesbrough](https://www.fotmob.com/ko/teams/8549/overview/middlesbrough)
[LBMatt Targett](https://www.fotmob.com/ko/players/538112/matt-targett)
임대
2025. 8. 27.
[Juventus](https://www.fotmob.com/ko/teams/9885/overview/juventus)[Gremio](https://www.fotmob.com/ko/teams/9769/overview/gremio)
[DMArthur](https://www.fotmob.com/ko/players/654044/arthur)
임대
2025. 8. 27.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Dortmund](https://www.fotmob.com/ko/teams/9789/overview/dortmund)
[AMCarney Chukwuemeka](https://www.fotmob.com/ko/players/1089685/carney-chukwuemeka)
€2000만
2025. 8. 26.
[Southampton](https://www.fotmob.com/ko/teams/8466/overview/southampton)[Everton](https://www.fotmob.com/ko/teams/8668/overview/everton)
[RWTyler Dibling](https://www.fotmob.com/ko/players/1292833/tyler-dibling)
€4050만
2025. 8. 26.
[Cagliari](https://www.fotmob.com/ko/teams/8529/overview/cagliari)[Fiorentina](https://www.fotmob.com/ko/teams/8535/overview/fiorentina)
[STRoberto Piccoli](https://www.fotmob.com/ko/players/1017401/roberto-piccoli)
€2500만
2025. 8. 26.
[Crystal Palace](https://www.fotmob.com/ko/teams/9826/overview/crystal-palace)[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)
[AMEberechi Eze](https://www.fotmob.com/ko/players/818975/eberechi-eze)
€6900만
2025. 8. 24.
[Dortmund](https://www.fotmob.com/ko/teams/9789/overview/dortmund)[M'gladbach](https://www.fotmob.com/ko/teams/9788/overview/mgladbach)
[AMGiovanni Reyna](https://www.fotmob.com/ko/players/1071179/giovanni-reyna)
€300만
2025. 8. 24.
[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)[Fenerbahçe](https://www.fotmob.com/ko/teams/8695/overview/fenerbahce)
[DMEdson Álvarez](https://www.fotmob.com/ko/players/783505/edson-alvarez)
€200만. 임대 중
2025. 8. 23.
[Lens](https://www.fotmob.com/ko/teams/8588/overview/lens)[Inter](https://www.fotmob.com/ko/teams/8636/overview/inter)
[CMAndy Diouf](https://www.fotmob.com/ko/players/1254297/andy-diouf)
€2500만
2025. 8. 23.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Villarreal](https://www.fotmob.com/ko/teams/10205/overview/villarreal)
[CBRenato Veiga](https://www.fotmob.com/ko/players/1343750/renato-veiga)
€2450만
2025. 8. 22.
[Juventus](https://www.fotmob.com/ko/teams/9885/overview/juventus)[Nottm Forest](https://www.fotmob.com/ko/teams/10203/overview/nottm-forest)
[DMDouglas Luiz](https://www.fotmob.com/ko/players/787350/douglas-luiz)
임대
2025. 8. 22.
[Sevilla](https://www.fotmob.com/ko/teams/8302/overview/sevilla)[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)
[CBLoic Badé](https://www.fotmob.com/ko/players/1119461/loic-bade)
€2500만
2025. 8. 21.
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Leeds](https://www.fotmob.com/ko/teams/8463/overview/leeds)
[LWNoah Okafor](https://www.fotmob.com/ko/players/915797/noah-okafor)
€2000만
2025. 8. 21.
[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)
[LWAmine Adli](https://www.fotmob.com/ko/players/1079557/amine-adli)
€2100만
2025. 8. 21.
[Lecce](https://www.fotmob.com/ko/teams/9888/overview/lecce)[Atalanta](https://www.fotmob.com/ko/teams/8524/overview/atalanta)
[STNikola Krstovic](https://www.fotmob.com/ko/players/833638/nikola-krstovic)
€2500만
2025. 8. 21.
[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)[Roma](https://www.fotmob.com/ko/teams/8686/overview/roma)
[RWLeon Bailey](https://www.fotmob.com/ko/players/671331/leon-bailey)
€300만. 임대 중
2025. 8. 20.
[Salzburg](https://www.fotmob.com/ko/teams/10013/overview/salzburg)[Fenerbahçe](https://www.fotmob.com/ko/teams/8695/overview/fenerbahce)
[RWDorgeles Nene](https://www.fotmob.com/ko/players/1230287/dorgeles-nene)
€1800만
2025. 8. 20.
[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)[Middlesbrough](https://www.fotmob.com/ko/teams/8549/overview/middlesbrough)
[AMSverre Halseth Nypan](https://www.fotmob.com/ko/players/1355509/sverre-halseth-nypan)
임대
2025. 8. 19.
[Inter](https://www.fotmob.com/ko/teams/8636/overview/inter)[Atalanta](https://www.fotmob.com/ko/teams/8524/overview/atalanta)
[AMNicola Zalewski](https://www.fotmob.com/ko/players/1053714/nicola-zalewski)
€1700만
2025. 8. 19.
[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)
[RWBen Gannon-Doak](https://www.fotmob.com/ko/players/1324871/ben-gannon-doak)
€2500만
2025. 8. 19.
[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)[Elche](https://www.fotmob.com/ko/teams/10268/overview/elche)
[STAndré Silva](https://www.fotmob.com/ko/players/388523/andre-silva)
€100만
2025. 8. 18.
[Rennes](https://www.fotmob.com/ko/teams/9851/overview/rennes)[Nottm Forest](https://www.fotmob.com/ko/teams/10203/overview/nottm-forest)
[STArnaud Kalimuendo-Muinga](https://www.fotmob.com/ko/players/1095445/arnaud-kalimuendo-muinga)
€3000만
2025. 8. 18.
[Dortmund](https://www.fotmob.com/ko/teams/9789/overview/dortmund)[FC Utrecht](https://www.fotmob.com/ko/teams/9908/overview/fc-utrecht)
[STSébastien Haller](https://www.fotmob.com/ko/players/352968/sebastien-haller)
자유 이적
2025. 8. 18.
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Panathinaikos](https://www.fotmob.com/ko/teams/10200/overview/panathinaikos)
[RBDavide Calabria](https://www.fotmob.com/ko/players/612755/davide-calabria)
자유 이적
2025. 8. 18.
[PSG](https://www.fotmob.com/ko/teams/9847/overview/psg)[Sunderland](https://www.fotmob.com/ko/teams/8472/overview/sunderland)
[CBNordi Mukiele](https://www.fotmob.com/ko/players/602304/nordi-mukiele)
€1200만
2025. 8. 18.
[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)[Newcastle](https://www.fotmob.com/ko/teams/10261/overview/newcastle)
[CMJacob Ramsey](https://www.fotmob.com/ko/players/1021929/jacob-ramsey)
€4000만
2025. 8. 18.
[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)[Nottm Forest](https://www.fotmob.com/ko/teams/10203/overview/nottm-forest)
[AMJames McAtee](https://www.fotmob.com/ko/players/1107648/james-mcatee)
€3500만
2025. 8. 17.
[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)[Brentford](https://www.fotmob.com/ko/teams/9937/overview/brentford)
[RWDango Ouattara](https://www.fotmob.com/ko/players/1250253/dango-ouattara)
€4860만
2025. 8. 17.
[Ipswich](https://www.fotmob.com/ko/teams/9902/overview/ipswich)[Nottm Forest](https://www.fotmob.com/ko/teams/10203/overview/nottm-forest)
[RWOmari Hutchinson](https://www.fotmob.com/ko/players/1215652/omari-hutchinson)
€4340만
2025. 8. 17.
[Bayern München](https://www.fotmob.com/ko/teams/9823/overview/bayern-munchen)[Al Nassr FC](https://www.fotmob.com/ko/teams/101918/overview/al-nassr-fc)
[RMKingsley Coman](https://www.fotmob.com/ko/players/429265/kingsley-coman)
밝혀지지 않음
2025. 8. 16.
[Parma](https://www.fotmob.com/ko/teams/10167/overview/parma)[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)
[CBGiovanni Leoni](https://www.fotmob.com/ko/players/1609209/giovanni-leoni)
€3500만
2025. 8. 16.
[Everton](https://www.fotmob.com/ko/teams/8668/overview/everton)[Leeds](https://www.fotmob.com/ko/teams/8463/overview/leeds)
[STDominic Calvert-Lewin](https://www.fotmob.com/ko/players/612150/dominic-calvert-lewin)
자유 이적
2025. 8. 15.
[Göztepe](https://www.fotmob.com/ko/teams/1925/overview/goztepe)[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)
[STRômulo](https://www.fotmob.com/ko/players/1314412/romulo)
€2000만
2025. 8. 15.
[Lens](https://www.fotmob.com/ko/teams/8588/overview/lens)[Nice](https://www.fotmob.com/ko/teams/9831/overview/nice)
[DMSalis Abdul Samed](https://www.fotmob.com/ko/players/1074642/salis-abdul-samed)
€250만
2025. 8. 15.
[Genoa](https://www.fotmob.com/ko/teams/10233/overview/genoa)[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)
[CBKoni De Winter](https://www.fotmob.com/ko/players/1200630/koni-de-winter)
€2000만
2025. 8. 14.
[Lille](https://www.fotmob.com/ko/teams/8639/overview/lille)[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)
[CBBafodé Diakité](https://www.fotmob.com/ko/players/979752/bafode-diakite)
€3500만
2025. 8. 13.
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Newcastle](https://www.fotmob.com/ko/teams/10261/overview/newcastle)
[CBMalick Thiaw](https://www.fotmob.com/ko/players/1137407/malick-thiaw)
€3600만
2025. 8. 13.
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Como](https://www.fotmob.com/ko/teams/10171/overview/como)
[STÁlvaro Morata](https://www.fotmob.com/ko/players/213501/alvaro-morata)
임대
2025. 8. 13.
[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)[Everton](https://www.fotmob.com/ko/teams/8668/overview/everton)
[LWJack Grealish](https://www.fotmob.com/ko/players/312765/jack-grealish)
임대
2025. 8. 13.
[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)[PSG](https://www.fotmob.com/ko/teams/9847/overview/psg)
[CBIlya Zabarnyi](https://www.fotmob.com/ko/players/1140003/ilya-zabarnyi)
€6300만
2025. 8. 12.
[Napoli](https://www.fotmob.com/ko/teams/9875/overview/napoli)[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)
[AMGiacomo Raspadori](https://www.fotmob.com/ko/players/951743/giacomo-raspadori)
€2200만
2025. 8. 11.
[Villarreal](https://www.fotmob.com/ko/teams/10205/overview/villarreal)[Valencia](https://www.fotmob.com/ko/teams/10267/overview/valencia)
[LMArnaut Danjuma](https://www.fotmob.com/ko/players/704151/arnaut-danjuma)
€50만
2025. 8. 10.
[Leicester](https://www.fotmob.com/ko/teams/8197/overview/leicester)[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)
[골키퍼Mads Hermansen](https://www.fotmob.com/ko/players/967941/mads-hermansen)
€2078만
2025. 8. 10.
[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)[Al Hilal](https://www.fotmob.com/ko/teams/2529/overview/al-hilal)
[STDarwin Núñez](https://www.fotmob.com/ko/players/950561/darwin-nunez)
€5300만
2025. 8. 10.
[VfB Stuttgart](https://www.fotmob.com/ko/teams/10269/overview/vfb-stuttgart)[Al Ahli](https://www.fotmob.com/ko/teams/2530/overview/al-ahli)
[AMEnzo Millot](https://www.fotmob.com/ko/players/1050859/enzo-millot)
€2800만
2025. 8. 10.
[Lille](https://www.fotmob.com/ko/teams/8639/overview/lille)[PSG](https://www.fotmob.com/ko/teams/9847/overview/psg)
[골키퍼Lucas Chevalier](https://www.fotmob.com/ko/players/1177131/lucas-chevalier)
€4000만
2025. 8. 10.
[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)
[STBenjamin Sesko](https://www.fotmob.com/ko/players/1073977/benjamin-sesko)
€7650만
2025. 8. 9.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Burnley](https://www.fotmob.com/ko/teams/8191/overview/burnley)
[STArmando Broja](https://www.fotmob.com/ko/players/1077975/armando-broja)
€2300만
2025. 8. 9.
[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)[Girona](https://www.fotmob.com/ko/teams/7732/overview/girona)
[CBVitor Reis](https://www.fotmob.com/ko/players/1580952/vitor-reis)
임대
2025. 8. 8.
[Leicester](https://www.fotmob.com/ko/teams/8197/overview/leicester)[Beşiktaş](https://www.fotmob.com/ko/teams/10188/overview/besiktas)
[DMWilfred Ndidi](https://www.fotmob.com/ko/players/533228/wilfred-ndidi)
€800만
2025. 8. 8.
[Nice](https://www.fotmob.com/ko/teams/9831/overview/nice)[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)
[RWEvann Guessand](https://www.fotmob.com/ko/players/1087966/evann-guessand)
€3000만
2025. 8. 8.
Free agent
[Villarreal](https://www.fotmob.com/ko/teams/10205/overview/villarreal)
[CMThomas Partey](https://www.fotmob.com/ko/players/434325/thomas-partey)
자유 이적
2025. 8. 8.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Burnley](https://www.fotmob.com/ko/teams/8191/overview/burnley)
[DMLesley Ugochukwu](https://www.fotmob.com/ko/players/1200631/lesley-ugochukwu)
€2878만
2025. 8. 7.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Everton](https://www.fotmob.com/ko/teams/8668/overview/everton)
[AMKiernan Dewsbury-Hall](https://www.fotmob.com/ko/players/886016/kiernan-dewsbury-hall)
€2865만
2025. 8. 7.
[Freiburg](https://www.fotmob.com/ko/teams/8358/overview/freiburg)[Frankfurt](https://www.fotmob.com/ko/teams/9810/overview/frankfurt)
[RWRitsu Doan](https://www.fotmob.com/ko/players/629805/ritsu-doan)
€2110만
2025. 8. 7.
[Tottenham](https://www.fotmob.com/ko/teams/8586/overview/tottenham)[LAFC](https://www.fotmob.com/ko/teams/867280/overview/lafc)
[STHeung-Min Son](https://www.fotmob.com/ko/players/212867/heung-min-son)
€2200만
2025. 8. 7.
Free agent
[Vancouver](https://www.fotmob.com/ko/teams/307691/overview/vancouver)
[AMThomas Müller](https://www.fotmob.com/ko/players/116772/thomas-muller)
자유 이적
2025. 8. 7.
[Juventus](https://www.fotmob.com/ko/teams/9885/overview/juventus)[Marseille](https://www.fotmob.com/ko/teams/8592/overview/marseille)
[RBTimothy Weah](https://www.fotmob.com/ko/players/889536/timothy-weah)
€100만. 임대 중
2025. 8. 7.
[Club Brugge](https://www.fotmob.com/ko/teams/8342/overview/club-brugge)[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)
[CMArdon Jashari](https://www.fotmob.com/ko/players/1163219/ardon-jashari)
€3600만
2025. 8. 7.
[Wolves](https://www.fotmob.com/ko/teams/8602/overview/wolves)[Real Sociedad](https://www.fotmob.com/ko/teams/8560/overview/real-sociedad)
[LWGonçalo Guedes](https://www.fotmob.com/ko/players/536455/goncalo-guedes)
€400만
2025. 8. 5.
[Bayern München](https://www.fotmob.com/ko/teams/9823/overview/bayern-munchen)[Tottenham](https://www.fotmob.com/ko/teams/8586/overview/tottenham)
[DMJoão Palhinha](https://www.fotmob.com/ko/players/524434/joao-palhinha)
임대
2025. 8. 4.
[Ajax](https://www.fotmob.com/ko/teams/8593/overview/ajax)[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)
[LBJorrel Hato](https://www.fotmob.com/ko/players/1413846/jorrel-hato)
€4300만
2025. 8. 4.
[Southampton](https://www.fotmob.com/ko/teams/8466/overview/southampton)[Newcastle](https://www.fotmob.com/ko/teams/10261/overview/newcastle)
[골키퍼Aaron Ramsdale](https://www.fotmob.com/ko/players/746395/aaron-ramsdale)
임대
2025. 8. 3.
[Feyenoord](https://www.fotmob.com/ko/teams/10235/overview/feyenoord)[Marseille](https://www.fotmob.com/ko/teams/8592/overview/marseille)
[LWIgor Paixão](https://www.fotmob.com/ko/players/1265963/igor-paixao)
€3000만
2025. 8. 2.
[Leicester](https://www.fotmob.com/ko/teams/8197/overview/leicester)[Wrexham](https://www.fotmob.com/ko/teams/9841/overview/wrexham)
[CBConor Coady](https://www.fotmob.com/ko/players/247761/conor-coady)
밝혀지지 않음
2025. 8. 2.
[Bayern München](https://www.fotmob.com/ko/teams/9823/overview/bayern-munchen)Free agent
[AMThomas Müller](https://www.fotmob.com/ko/players/116772/thomas-muller)
자유 이적
2025. 8. 2.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Strasbourg](https://www.fotmob.com/ko/teams/9848/overview/strasbourg)
[CBMamadou Sarr](https://www.fotmob.com/ko/players/1426170/mamadou-sarr)
임대
2025. 8. 1.
[NEC Nijmegen](https://www.fotmob.com/ko/teams/8464/overview/nec-nijmegen)[Sunderland](https://www.fotmob.com/ko/teams/8472/overview/sunderland)
[골키퍼Robin Roefs](https://www.fotmob.com/ko/players/1125720/robin-roefs)
€1050만
2025. 8. 1.
[Union St.Gilloise](https://www.fotmob.com/ko/teams/7978/overview/union-stgilloise)[Benfica](https://www.fotmob.com/ko/teams/9772/overview/benfica)
[STFranjo Ivanovic](https://www.fotmob.com/ko/players/1406419/franjo-ivanovic)
€2200만
2025. 8. 1.
[Napoli](https://www.fotmob.com/ko/teams/9875/overview/napoli)[Galatasaray](https://www.fotmob.com/ko/teams/8637/overview/galatasaray)
[STVictor Osimhen](https://www.fotmob.com/ko/players/687681/victor-osimhen)
€7500만
2025. 8. 1.
[Nantes](https://www.fotmob.com/ko/teams/9830/overview/nantes)Neom SC
[CBNathan Zézé](https://www.fotmob.com/ko/players/1429120/nathan-zeze)
€2000만
2025. 8. 1.
[Beşiktaş](https://www.fotmob.com/ko/teams/10188/overview/besiktas)[Spartak](https://www.fotmob.com/ko/teams/8643/overview/spartak)
[AMGedson Fernandes](https://www.fotmob.com/ko/players/747785/gedson-fernandes)
€2050만
2025. 8. 1.
[Bologna](https://www.fotmob.com/ko/teams/9857/overview/bologna)[Nottm Forest](https://www.fotmob.com/ko/teams/10203/overview/nottm-forest)
[RWDan Ndoye](https://www.fotmob.com/ko/players/1022649/dan-ndoye)
€4200만
2025. 7. 31.
[PSG](https://www.fotmob.com/ko/teams/9847/overview/psg)[Fenerbahçe](https://www.fotmob.com/ko/teams/8695/overview/fenerbahce)
[CBMilan Skriniar](https://www.fotmob.com/ko/players/309328/milan-skriniar)
€900만
2025. 7. 31.
[Burnley](https://www.fotmob.com/ko/teams/8191/overview/burnley)[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)
[골키퍼James Trafford](https://www.fotmob.com/ko/players/1187213/james-trafford)
€3120만
2025. 7. 30.
[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)[Sunderland](https://www.fotmob.com/ko/teams/8472/overview/sunderland)
[DMGranit Xhaka](https://www.fotmob.com/ko/players/207236/granit-xhaka)
€1500만
2025. 7. 30.
[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)[Bayern München](https://www.fotmob.com/ko/teams/9823/overview/bayern-munchen)
[LWLuis Díaz](https://www.fotmob.com/ko/players/860914/luis-diaz)
€7100만
2025. 7. 30.
[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)[Flamengo](https://www.fotmob.com/ko/teams/9770/overview/flamengo)
[LWSamuel Dias Lino](https://www.fotmob.com/ko/players/1082941/samuel-dias-lino)
€2200만
2025. 7. 30.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Al Nassr FC](https://www.fotmob.com/ko/teams/101918/overview/al-nassr-fc)
[AMJoao Félix](https://www.fotmob.com/ko/players/794427/joao-felix)
€3000만
2025. 7. 29.
[Southampton](https://www.fotmob.com/ko/teams/8466/overview/southampton)[FC Porto](https://www.fotmob.com/ko/teams/9773/overview/fc-porto)
[CBJan Bednarek](https://www.fotmob.com/ko/players/490868/jan-bednarek)
€760만
2025. 7. 29.
[Flamengo](https://www.fotmob.com/ko/teams/9770/overview/flamengo)[Roma](https://www.fotmob.com/ko/teams/8686/overview/roma)
[LWBWesley](https://www.fotmob.com/ko/players/1320176/wesley)
€2500만
2025. 7. 29.
[Almeria](https://www.fotmob.com/ko/teams/9865/overview/almeria)[Sporting CP](https://www.fotmob.com/ko/teams/9768/overview/sporting-cp)
[STLuis Suárez](https://www.fotmob.com/ko/players/792303/luis-suarez)
€2200만
2025. 7. 29.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Strasbourg](https://www.fotmob.com/ko/teams/9848/overview/strasbourg)
[골키퍼Mike Penders](https://www.fotmob.com/ko/players/1319972/mike-penders)
임대
2025. 7. 28.
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Flamengo](https://www.fotmob.com/ko/teams/9770/overview/flamengo)
[RBEmerson Royal](https://www.fotmob.com/ko/players/797908/emerson-royal)
€900만
2025. 7. 27.
[Torino](https://www.fotmob.com/ko/teams/9804/overview/torino)[Napoli](https://www.fotmob.com/ko/teams/9875/overview/napoli)
[골키퍼Vanja Milinkovic-Savic](https://www.fotmob.com/ko/players/543021/vanja-milinkovic-savic)
임대
2025. 7. 27.
[Sporting CP](https://www.fotmob.com/ko/teams/9768/overview/sporting-cp)[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)
[STViktor Gyökeres](https://www.fotmob.com/ko/players/664500/viktor-gyokeres)
€6350만
2025. 7. 27.
[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)[Inter Miami CF](https://www.fotmob.com/ko/teams/960720/overview/inter-miami-cf)
[CMRodrigo De Paul](https://www.fotmob.com/ko/players/324578/rodrigo-de-paul)
임대
2025. 7. 26.
[Inter](https://www.fotmob.com/ko/teams/8636/overview/inter)[Club Brugge](https://www.fotmob.com/ko/teams/8342/overview/club-brugge)
[DMAleksandar Stankovic](https://www.fotmob.com/ko/players/1410437/aleksandar-stankovic)
€900만
2025. 7. 25.
[Feyenoord](https://www.fotmob.com/ko/teams/10235/overview/feyenoord)[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)
[CBDávid Hancko](https://www.fotmob.com/ko/players/727897/david-hancko)
€3000만
2025. 7. 25.
[Valencia](https://www.fotmob.com/ko/teams/10267/overview/valencia)[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)
[CBCristhian Mosquera](https://www.fotmob.com/ko/players/1298907/cristhian-mosquera)
€1500만
2025. 7. 25.
[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)
[LMPervis Estupinán](https://www.fotmob.com/ko/players/688278/pervis-estupinan)
€1700만
2025. 7. 24.
[Napoli](https://www.fotmob.com/ko/teams/9875/overview/napoli)[Wolfsburg](https://www.fotmob.com/ko/teams/8721/overview/wolfsburg)
[AMJesper Lindstrøm](https://www.fotmob.com/ko/players/958335/jesper-lindstrom)
€150만. 임대 중
2025. 7. 24.
[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)[Flamengo](https://www.fotmob.com/ko/teams/9770/overview/flamengo)
[DMSaúl](https://www.fotmob.com/ko/players/309334/saul)
자유 이적
2025. 7. 24.
[Al Ahli](https://www.fotmob.com/ko/teams/2530/overview/al-ahli)[Al-Sadd](https://www.fotmob.com/ko/teams/101895/overview/al-sadd)
[AMRoberto Firmino](https://www.fotmob.com/ko/players/242709/roberto-firmino)
2025. 7. 24.
[Frankfurt](https://www.fotmob.com/ko/teams/9810/overview/frankfurt)[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)
[STHugo Ekitiké](https://www.fotmob.com/ko/players/1197030/hugo-ekitike)
€9500만
2025. 7. 24.
[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)[Barcelona](https://www.fotmob.com/ko/teams/8634/overview/barcelona)
[LWMarcus Rashford](https://www.fotmob.com/ko/players/696365/marcus-rashford)
임대
2025. 7. 24.
[Almeria](https://www.fotmob.com/ko/teams/9865/overview/almeria)[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)
[CBMarc Pubill](https://www.fotmob.com/ko/players/1323897/marc-pubill)
€1600만
2025. 7. 23.
[FC København](https://www.fotmob.com/ko/teams/8391/overview/fc-kobenhavn)[FC Porto](https://www.fotmob.com/ko/teams/9773/overview/fc-porto)
[CMVictor Froholdt](https://www.fotmob.com/ko/players/1436856/victor-froholdt)
€2000만
2025. 7. 23.
[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)[Roma](https://www.fotmob.com/ko/teams/8686/overview/roma)
[STEvan Ferguson](https://www.fotmob.com/ko/players/1068482/evan-ferguson)
€300만. 임대 중
2025. 7. 23.
[Palmeiras](https://www.fotmob.com/ko/teams/10283/overview/palmeiras)[Benfica](https://www.fotmob.com/ko/teams/9772/overview/benfica)
[DMRichard Ríos](https://www.fotmob.com/ko/players/1174630/richard-rios)
€2700만
2025. 7. 23.
[FC Porto](https://www.fotmob.com/ko/teams/9773/overview/fc-porto)[Juventus](https://www.fotmob.com/ko/teams/9885/overview/juventus)
[AMFrancisco Conceição](https://www.fotmob.com/ko/players/1185336/francisco-conceicao)
€3200만
2025. 7. 23.
[Nice](https://www.fotmob.com/ko/teams/9831/overview/nice)Al-Diraiyah
[STGaëtan Laborde](https://www.fotmob.com/ko/players/492158/gaetan-laborde)
€400만
2025. 7. 22.
[Hoffenheim](https://www.fotmob.com/ko/teams/8226/overview/hoffenheim)[Leeds](https://www.fotmob.com/ko/teams/8463/overview/leeds)
[CMAnton Stach](https://www.fotmob.com/ko/players/881735/anton-stach)
€2000만
2025. 7. 22.
[Brentford](https://www.fotmob.com/ko/teams/9937/overview/brentford)[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)
[AMBryan Mbeumo](https://www.fotmob.com/ko/players/923312/bryan-mbeumo)
€7500만
2025. 7. 22.
[Atalanta](https://www.fotmob.com/ko/teams/8524/overview/atalanta)Al Qadasiya
[STMateo Retegui](https://www.fotmob.com/ko/players/905546/mateo-retegui)
€6800만
2025. 7. 22.
[Lyon](https://www.fotmob.com/ko/teams/9748/overview/lyon)Neom SC
[LMSaïd Benrahma](https://www.fotmob.com/ko/players/491883/said-benrahma)
€1200만
2025. 7. 22.
[Lens](https://www.fotmob.com/ko/teams/8588/overview/lens)[Roma](https://www.fotmob.com/ko/teams/8686/overview/roma)
[DMNeil El Aynaoui](https://www.fotmob.com/ko/players/1274060/neil-el-aynaoui)
€2350만
2025. 7. 21.
[Bologna](https://www.fotmob.com/ko/teams/9857/overview/bologna)[Napoli](https://www.fotmob.com/ko/teams/9875/overview/napoli)
[CBSam Beukema](https://www.fotmob.com/ko/players/873573/sam-beukema)
€3100만
2025. 7. 21.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)
[RWNoni Madueke](https://www.fotmob.com/ko/players/1084981/noni-madueke)
€5500만
2025. 7. 19.
[Nottm Forest](https://www.fotmob.com/ko/teams/10203/overview/nottm-forest)[Botafogo RJ](https://www.fotmob.com/ko/teams/8517/overview/botafogo-rj)
[DMDanilo](https://www.fotmob.com/ko/players/1181700/danilo)
€2300만
2025. 7. 19.
[Udinese](https://www.fotmob.com/ko/teams/8600/overview/udinese)[Napoli](https://www.fotmob.com/ko/teams/9875/overview/napoli)
[STLorenzo Lucca](https://www.fotmob.com/ko/players/1212630/lorenzo-lucca)
€900만
2025. 7. 18.
[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)[Como](https://www.fotmob.com/ko/teams/10171/overview/como)
[DMMáximo Perrone](https://www.fotmob.com/ko/players/1336582/maximo-perrone)
€1300만
2025. 7. 18.
[Rosenborg](https://www.fotmob.com/ko/teams/8422/overview/rosenborg)[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)
[AMSverre Halseth Nypan](https://www.fotmob.com/ko/players/1355509/sverre-halseth-nypan)
€1500만
2025. 7. 18.
[Botafogo RJ](https://www.fotmob.com/ko/teams/8517/overview/botafogo-rj)[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)
[LMThiago Almada](https://www.fotmob.com/ko/players/955271/thiago-almada)
€2500만
2025. 7. 18.
[PSV Eindhoven](https://www.fotmob.com/ko/teams/8640/overview/psv-eindhoven)[Napoli](https://www.fotmob.com/ko/teams/9875/overview/napoli)
[LWNoa Lang](https://www.fotmob.com/ko/players/837341/noa-lang)
€2500만
2025. 7. 17.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)
[골키퍼Djordje Petrovic](https://www.fotmob.com/ko/players/1067256/djordje-petrovic)
€2900만
2025. 7. 17.
[PSV Eindhoven](https://www.fotmob.com/ko/teams/8640/overview/psv-eindhoven)[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)
[RWJohan Bakayoko](https://www.fotmob.com/ko/players/1203194/johan-bakayoko)
2025. 7. 17.
[Real Betis](https://www.fotmob.com/ko/teams/8603/overview/real-betis)[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)
[CMJohnny Cardoso](https://www.fotmob.com/ko/players/1173678/johnny-cardoso)
€3000만
2025. 7. 16.
[Leganes](https://www.fotmob.com/ko/teams/7854/overview/leganes)[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)
[RWYan Diomande](https://www.fotmob.com/ko/players/1735453/yan-diomande)
€2010만
2025. 7. 16.
[Slavia Prague](https://www.fotmob.com/ko/teams/7787/overview/slavia-prague)[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)
[LBMalick Diouf](https://www.fotmob.com/ko/players/1451265/malick-diouf)
€2200만
2025. 7. 16.
Free agent
[Brentford](https://www.fotmob.com/ko/teams/9937/overview/brentford)
[DMJordan Henderson](https://www.fotmob.com/ko/players/156008/jordan-henderson)
자유 이적
2025. 7. 15.
[Benfica](https://www.fotmob.com/ko/teams/9772/overview/benfica)[Real Madrid](https://www.fotmob.com/ko/teams/8633/overview/real-madrid)
[LBAlvaro Carreras](https://www.fotmob.com/ko/players/1190025/alvaro-carreras)
€5000만
2025. 7. 15.
[Norwich](https://www.fotmob.com/ko/teams/9850/overview/norwich)[FC Porto](https://www.fotmob.com/ko/teams/9773/overview/fc-porto)
[LWBorja Sainz](https://www.fotmob.com/ko/players/1083204/borja-sainz)
€1350만
2025. 7. 14.
[RB Leipzig](https://www.fotmob.com/ko/teams/178475/overview/rb-leipzig)[Hamburger SV](https://www.fotmob.com/ko/teams/9790/overview/hamburger-sv)
[STYussuf Poulsen](https://www.fotmob.com/ko/players/266527/yussuf-poulsen)
€100만
2025. 7. 14.
[PSV Eindhoven](https://www.fotmob.com/ko/teams/8640/overview/psv-eindhoven)[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)
[AMMalik Tillman](https://www.fotmob.com/ko/players/1126058/malik-tillman)
€3510만
2025. 7. 12.
[Benfica](https://www.fotmob.com/ko/teams/9772/overview/benfica)[Beşiktaş](https://www.fotmob.com/ko/teams/10188/overview/besiktas)
[AMOrkun Kökcü](https://www.fotmob.com/ko/players/935409/orkun-kokcu)
임대
2025. 7. 12.
[Nottm Forest](https://www.fotmob.com/ko/teams/10203/overview/nottm-forest)[Newcastle](https://www.fotmob.com/ko/teams/10261/overview/newcastle)
[RWAnthony Elanga](https://www.fotmob.com/ko/players/1050166/anthony-elanga)
밝혀지지 않음
2025. 7. 12.
[Albacete](https://www.fotmob.com/ko/teams/8393/overview/albacete)[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)
[STChristian Kofane](https://www.fotmob.com/ko/players/1705081/christian-kofane)
€500만
2025. 7. 11.
[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)[Tottenham](https://www.fotmob.com/ko/teams/8586/overview/tottenham)
[RWMohammed Kudus](https://www.fotmob.com/ko/players/891743/mohammed-kudus)
밝혀지지 않음
2025. 7. 11.
[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)[Sunderland](https://www.fotmob.com/ko/teams/8472/overview/sunderland)
[LWSimon Adingra](https://www.fotmob.com/ko/players/1227012/simon-adingra)
€2400만
2025. 7. 11.
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Al Hilal](https://www.fotmob.com/ko/teams/2529/overview/al-hilal)
[LBTheo Hernández](https://www.fotmob.com/ko/players/724371/theo-hernandez)
€2500만
2025. 7. 11.
Free agent
[Bologna](https://www.fotmob.com/ko/teams/9857/overview/bologna)
[STCiro Immobile](https://www.fotmob.com/ko/players/161660/ciro-immobile)
자유 이적
2025. 7. 11.
[Ajax](https://www.fotmob.com/ko/teams/8593/overview/ajax)Free agent
[DMJordan Henderson](https://www.fotmob.com/ko/players/156008/jordan-henderson)
자유 이적
2025. 7. 10.
[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)[Tigres](https://www.fotmob.com/ko/teams/8561/overview/tigres)
[AMÁngel Correa](https://www.fotmob.com/ko/players/432950/angel-correa)
€800만
2025. 7. 10.
[Villarreal](https://www.fotmob.com/ko/teams/10205/overview/villarreal)[Everton](https://www.fotmob.com/ko/teams/8668/overview/everton)
[STThierno Barry](https://www.fotmob.com/ko/players/1398392/thierno-barry)
€3000만
2025. 7. 10.
[Club Brugge](https://www.fotmob.com/ko/teams/8342/overview/club-brugge)[Sunderland](https://www.fotmob.com/ko/teams/8472/overview/sunderland)
[RWChemsdine Talbi](https://www.fotmob.com/ko/players/1368654/chemsdine-talbi)
€2000만
2025. 7. 9.
[PAOK Thessaloniki](https://www.fotmob.com/ko/teams/8619/overview/paok-thessaloniki)[Deportivo Alaves](https://www.fotmob.com/ko/teams/9866/overview/deportivo-alaves)
[RBJonny Otto](https://www.fotmob.com/ko/players/360918/jonny-otto)
자유 이적
2025. 7. 9.
[Lille](https://www.fotmob.com/ko/teams/8639/overview/lille)[Leeds](https://www.fotmob.com/ko/teams/8463/overview/leeds)
[LWBGabriel Gudmundsson](https://www.fotmob.com/ko/players/744494/gabriel-gudmundsson)
€1160만
2025. 7. 9.
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Lecce](https://www.fotmob.com/ko/teams/9888/overview/lecce)
[STFrancesco Camarda](https://www.fotmob.com/ko/players/1554575/francesco-camarda)
임대
2025. 7. 8.
[Al Nassr FC](https://www.fotmob.com/ko/teams/101918/overview/al-nassr-fc)[Fenerbahçe](https://www.fotmob.com/ko/teams/8695/overview/fenerbahce)
[STJhon Durán](https://www.fotmob.com/ko/players/1088066/jhon-duran)
임대
2025. 7. 7.
[Real Sociedad](https://www.fotmob.com/ko/teams/8560/overview/real-sociedad)[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)
[CMMartín Zubimendi](https://www.fotmob.com/ko/players/1031325/martin-zubimendi)
€6000만
2025. 7. 6.
[Club Brugge](https://www.fotmob.com/ko/teams/8342/overview/club-brugge)[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)
[LBMaxim De Cuyper](https://www.fotmob.com/ko/players/1134871/maxim-de-cuyper)
€2000만
2025. 7. 6.
[Botafogo RJ](https://www.fotmob.com/ko/teams/8517/overview/botafogo-rj)[Nottm Forest](https://www.fotmob.com/ko/teams/10203/overview/nottm-forest)
[STIgor Jesus](https://www.fotmob.com/ko/players/1082102/igor-jesus)
€1160만
2025. 7. 6.
[Dortmund](https://www.fotmob.com/ko/teams/9789/overview/dortmund)[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)
[LWJamie Gittens](https://www.fotmob.com/ko/players/1113692/jamie-gittens)
€6440만
2025. 7. 6.
[Parma](https://www.fotmob.com/ko/teams/10167/overview/parma)[Inter](https://www.fotmob.com/ko/teams/8636/overview/inter)
[STAnge-Yoan Bonny](https://www.fotmob.com/ko/players/1199383/ange-yoan-bonny)
€2300만
2025. 7. 5.
[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)[Burnley](https://www.fotmob.com/ko/teams/8191/overview/burnley)
[RBKyle Walker](https://www.fotmob.com/ko/players/159833/kyle-walker)
밝혀지지 않음
2025. 7. 5.
[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)Free agent
[CMChristian Eriksen](https://www.fotmob.com/ko/players/157723/christian-eriksen)
자유 이적
2025. 7. 5.
[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)Free agent
[CBVictor Nilsson Lindelöf](https://www.fotmob.com/ko/players/258269/victor-nilsson-lindelof)
자유 이적
2025. 7. 5.
[Tottenham](https://www.fotmob.com/ko/teams/8586/overview/tottenham)Free agent
[LBSergio Reguilón](https://www.fotmob.com/ko/players/724436/sergio-reguilon)
자유 이적
2025. 7. 5.
[Lille](https://www.fotmob.com/ko/teams/8639/overview/lille)[Juventus](https://www.fotmob.com/ko/teams/9885/overview/juventus)
[STJonathan David](https://www.fotmob.com/ko/players/939569/jonathan-david)
자유 이적
2025. 7. 5.
[Mainz](https://www.fotmob.com/ko/teams/9905/overview/mainz)[Frankfurt](https://www.fotmob.com/ko/teams/9810/overview/frankfurt)
[STJonathan Burkardt](https://www.fotmob.com/ko/players/947901/jonathan-burkardt)
€2110만
2025. 7. 5.
[Flamengo](https://www.fotmob.com/ko/teams/9770/overview/flamengo)[Zenit](https://www.fotmob.com/ko/teams/8698/overview/zenit)
[DMGérson](https://www.fotmob.com/ko/players/580604/gerson)
€2510만
2025. 7. 5.
[Beşiktaş](https://www.fotmob.com/ko/teams/10188/overview/besiktas)Free agent
[STCiro Immobile](https://www.fotmob.com/ko/players/161660/ciro-immobile)
2025. 7. 5.
[Union St.Gilloise](https://www.fotmob.com/ko/teams/7978/overview/union-stgilloise)[Sunderland](https://www.fotmob.com/ko/teams/8472/overview/sunderland)
[CMNoah Sadiki](https://www.fotmob.com/ko/players/1359649/noah-sadiki)
€1700만
2025. 7. 5.
[Genoa](https://www.fotmob.com/ko/teams/10233/overview/genoa)[Atalanta](https://www.fotmob.com/ko/teams/8524/overview/atalanta)
[CBHonest Ahanor](https://www.fotmob.com/ko/players/1669629/honest-ahanor)
€1600만
2025. 7. 4.
[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)[Vasco da Gama](https://www.fotmob.com/ko/teams/10276/overview/vasco-da-gama)
[AMPhilippe Coutinho](https://www.fotmob.com/ko/players/184536/philippe-coutinho)
자유 이적
2025. 7. 4.
[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)Free agent
[CBTakehiro Tomiyasu](https://www.fotmob.com/ko/players/664444/takehiro-tomiyasu)
2025. 7. 4.
[Torino](https://www.fotmob.com/ko/teams/9804/overview/torino)[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)
[CMSamuele Ricci](https://www.fotmob.com/ko/players/941656/samuele-ricci)
€2300만
2025. 7. 4.
[Feyenoord](https://www.fotmob.com/ko/teams/10235/overview/feyenoord)[Brentford](https://www.fotmob.com/ko/teams/9937/overview/brentford)
[CMAntoni Milambo](https://www.fotmob.com/ko/players/1276312/antoni-milambo)
€200만
2025. 7. 4.
[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)Free agent
[CBKurt Zouma](https://www.fotmob.com/ko/players/281207/kurt-zouma)
자유 이적
2025. 7. 3.
[Everton](https://www.fotmob.com/ko/teams/8668/overview/everton)Free agent
[STDominic Calvert-Lewin](https://www.fotmob.com/ko/players/612150/dominic-calvert-lewin)
자유 이적
2025. 7. 3.
[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)Free agent
[CMThomas Partey](https://www.fotmob.com/ko/players/434325/thomas-partey)
자유 이적
2025. 7. 3.
[Lyon](https://www.fotmob.com/ko/teams/9748/overview/lyon)Neom SC
[STAlexandre Lacazette](https://www.fotmob.com/ko/players/169193/alexandre-lacazette)
자유 이적
2025. 7. 3.
[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)
[STJoão Pedro](https://www.fotmob.com/ko/players/1021382/joao-pedro)
€6370만
2025. 7. 3.
[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)[Strasbourg](https://www.fotmob.com/ko/teams/9848/overview/strasbourg)
[DMValentín Barco](https://www.fotmob.com/ko/players/1272440/valentin-barco)
€1000만
2025. 7. 3.
[Lens](https://www.fotmob.com/ko/teams/8588/overview/lens)[Marseille](https://www.fotmob.com/ko/teams/8592/overview/marseille)
[CBFacundo Medina](https://www.fotmob.com/ko/players/812652/facundo-medina)
임대
2025. 7. 3.
[Real Betis](https://www.fotmob.com/ko/teams/8603/overview/real-betis)[Como](https://www.fotmob.com/ko/teams/10171/overview/como)
[LWJesús Rodríguez](https://www.fotmob.com/ko/players/1624039/jesus-rodriguez)
€2250만
2025. 7. 3.
[Southampton](https://www.fotmob.com/ko/teams/8466/overview/southampton)[Atalanta](https://www.fotmob.com/ko/teams/8524/overview/atalanta)
[AMKamaldeen Sulemana](https://www.fotmob.com/ko/players/1130691/kamaldeen-sulemana)
€1700만
2025. 7. 3.
[Villarreal](https://www.fotmob.com/ko/teams/10205/overview/villarreal)[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)
[LMÁlex Baena](https://www.fotmob.com/ko/players/942372/alex-baena)
€4500만
2025. 7. 2.
[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)
[CBJarell Quansah](https://www.fotmob.com/ko/players/1107620/jarell-quansah)
€3510만
2025. 7. 2.
[FC Groningen](https://www.fotmob.com/ko/teams/8674/overview/fc-groningen)[Feyenoord](https://www.fotmob.com/ko/teams/10235/overview/feyenoord)
[DMLuciano Valente](https://www.fotmob.com/ko/players/1256180/luciano-valente)
€675만
2025. 7. 2.
[Atalanta](https://www.fotmob.com/ko/teams/8524/overview/atalanta)[Atletico Madrid](https://www.fotmob.com/ko/teams/9906/overview/atletico-madrid)
[LBMatteo Ruggeri](https://www.fotmob.com/ko/players/1051097/matteo-ruggeri)
€1700만
2025. 7. 2.
[Strasbourg](https://www.fotmob.com/ko/teams/9848/overview/strasbourg)[Sunderland](https://www.fotmob.com/ko/teams/8472/overview/sunderland)
[CMHabib Diarra](https://www.fotmob.com/ko/players/1285866/habib-diarra)
€3150만
2025. 7. 2.
[Toronto](https://www.fotmob.com/ko/teams/56453/overview/toronto)Free agent
[AMLorenzo Insigne](https://www.fotmob.com/ko/players/193441/lorenzo-insigne)
자유 이적
2025. 7. 2.
[Roma](https://www.fotmob.com/ko/teams/8686/overview/roma)[Beşiktaş](https://www.fotmob.com/ko/teams/10188/overview/besiktas)
[STTammy Abraham](https://www.fotmob.com/ko/players/749661/tammy-abraham)
임대
2025. 7. 2.
[Fiorentina](https://www.fotmob.com/ko/teams/8535/overview/fiorentina)[Juventus](https://www.fotmob.com/ko/teams/9885/overview/juventus)
[Nico Gonzalez](https://www.fotmob.com/ko/players/1670274/nico-gonzalez)
€2800만
2025. 7. 2.
[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)[Atalanta](https://www.fotmob.com/ko/teams/8524/overview/atalanta)
[CBOdilon Kossounou](https://www.fotmob.com/ko/players/1014496/odilon-kossounou)
€2000만
2025. 7. 2.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)
[골키퍼Kepa Arrizabalaga](https://www.fotmob.com/ko/players/317564/kepa-arrizabalaga)
€500만
2025. 7. 1.
[Union Berlin](https://www.fotmob.com/ko/teams/8149/overview/union-berlin)[Fiorentina](https://www.fotmob.com/ko/teams/8535/overview/fiorentina)
[LBRobin Gosens](https://www.fotmob.com/ko/players/518346/robin-gosens)
€700만
2025. 7. 1.
[Newcastle](https://www.fotmob.com/ko/teams/10261/overview/newcastle)[Juventus](https://www.fotmob.com/ko/teams/9885/overview/juventus)
[CBLloyd Kelly](https://www.fotmob.com/ko/players/819215/lloyd-kelly)
€1700만
2025. 7. 1.
[Barcelona](https://www.fotmob.com/ko/teams/8634/overview/barcelona)[Monaco](https://www.fotmob.com/ko/teams/9829/overview/monaco)
[AMAnsu Fati](https://www.fotmob.com/ko/players/1086012/ansu-fati)
임대
2025. 7. 1.
[Celta Vigo](https://www.fotmob.com/ko/teams/9910/overview/celta-vigo)[Wolves](https://www.fotmob.com/ko/teams/8602/overview/wolves)
[STJørgen Strand Larsen](https://www.fotmob.com/ko/players/821100/jorgen-strand-larsen)
€2700만
2025. 7. 1.
[Getafe](https://www.fotmob.com/ko/teams/8305/overview/getafe)Free agent
[RBJuan Bernat](https://www.fotmob.com/ko/players/282691/juan-bernat)
2025. 7. 1.
[Dortmund](https://www.fotmob.com/ko/teams/9789/overview/dortmund)[FC København](https://www.fotmob.com/ko/teams/8391/overview/fc-kobenhavn)
[STYoussoufa Moukoko](https://www.fotmob.com/ko/players/1174708/youssoufa-moukoko)
€510만
2025. 6. 29.
Free agent
[Monaco](https://www.fotmob.com/ko/teams/9829/overview/monaco)
[CMPaul Pogba](https://www.fotmob.com/ko/players/248453/paul-pogba)
자유 이적
2025. 6. 29.
[Feyenoord](https://www.fotmob.com/ko/teams/10235/overview/feyenoord)[Burnley](https://www.fotmob.com/ko/teams/8191/overview/burnley)
[LBQuilindschy Hartman](https://www.fotmob.com/ko/players/1393669/quilindschy-hartman)
€1200만
2025. 6. 26.
[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)
[LBMilos Kerkez](https://www.fotmob.com/ko/players/1195281/milos-kerkez)
밝혀지지 않음
2025. 6. 26.
[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)[Rangers](https://www.fotmob.com/ko/teams/8548/overview/rangers)
[RBMax Aarons](https://www.fotmob.com/ko/players/956621/max-aarons)
임대
2025. 6. 26.
[Roma](https://www.fotmob.com/ko/teams/8686/overview/roma)[Inter](https://www.fotmob.com/ko/teams/8636/overview/inter)
[AMNicola Zalewski](https://www.fotmob.com/ko/players/1053714/nicola-zalewski)
€650만
2025. 6. 26.
[Udinese](https://www.fotmob.com/ko/teams/8600/overview/udinese)[Leeds](https://www.fotmob.com/ko/teams/8463/overview/leeds)
[CBJaka Bijol](https://www.fotmob.com/ko/players/861805/jaka-bijol)
€2200만
2025. 6. 24.
[Las Palmas](https://www.fotmob.com/ko/teams/8306/overview/las-palmas)[Villarreal](https://www.fotmob.com/ko/teams/10205/overview/villarreal)
[LWAlberto Moleiro](https://www.fotmob.com/ko/players/1184694/alberto-moleiro)
€1600만
2025. 6. 21.
[Celta Vigo](https://www.fotmob.com/ko/teams/9910/overview/celta-vigo)[Wolves](https://www.fotmob.com/ko/teams/8602/overview/wolves)
[AMFer Lopez](https://www.fotmob.com/ko/players/1573122/fer-lopez)
€2300만
2025. 6. 21.
[Lens](https://www.fotmob.com/ko/teams/8588/overview/lens)[Tottenham](https://www.fotmob.com/ko/teams/8586/overview/tottenham)
[CBKevin Danso](https://www.fotmob.com/ko/players/754126/kevin-danso)
€2500만
2025. 6. 21.
[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)
[AMFlorian Wirtz](https://www.fotmob.com/ko/players/1152455/florian-wirtz)
€1.3억
2025. 6. 21.
[Espanyol](https://www.fotmob.com/ko/teams/8558/overview/espanyol)[Barcelona](https://www.fotmob.com/ko/teams/8634/overview/barcelona)
[골키퍼Joan Garcia](https://www.fotmob.com/ko/players/1167220/joan-garcia)
€2500만
2025. 6. 20.
[Dinamo Zagreb](https://www.fotmob.com/ko/teams/10156/overview/dinamo-zagreb)[Como](https://www.fotmob.com/ko/teams/10171/overview/como)
[AMMartin Baturina](https://www.fotmob.com/ko/players/1215064/martin-baturina)
€1700만
2025. 6. 17.
[Bayern München](https://www.fotmob.com/ko/teams/9823/overview/bayern-munchen)[Tottenham](https://www.fotmob.com/ko/teams/8586/overview/tottenham)
[LWMathys Tel](https://www.fotmob.com/ko/players/1288111/mathys-tel)
€3600만
2025. 6. 15.
[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)[Atalanta](https://www.fotmob.com/ko/teams/8524/overview/atalanta)
[CBOdilon Kossounou](https://www.fotmob.com/ko/players/1014496/odilon-kossounou)
밝혀지지 않음
2025. 6. 14.
[River Plate](https://www.fotmob.com/ko/teams/10076/overview/river-plate)[Real Madrid](https://www.fotmob.com/ko/teams/8633/overview/real-madrid)
[RWFranco Mastantuono](https://www.fotmob.com/ko/players/1607566/franco-mastantuono)
€4500만
2025. 6. 13.
[Olympiacos](https://www.fotmob.com/ko/teams/8638/overview/olympiacos)[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)
[AMCharalampos Kostoulas](https://www.fotmob.com/ko/players/1561249/charalampos-kostoulas)
€3500만
2025. 6. 13.
[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)[Napoli](https://www.fotmob.com/ko/teams/9875/overview/napoli)
[AMKevin De Bruyne](https://www.fotmob.com/ko/players/169200/kevin-de-bruyne)
자유 이적
2025. 6. 13.
[Bayern München](https://www.fotmob.com/ko/teams/9823/overview/bayern-munchen)[Galatasaray](https://www.fotmob.com/ko/teams/8637/overview/galatasaray)
[RWLeroy Sané](https://www.fotmob.com/ko/players/530859/leroy-sane)
자유 이적
2025. 6. 12.
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)
[DMTijjani Reijnders](https://www.fotmob.com/ko/players/868344/tijjani-reijnders)
밝혀지지 않음
2025. 6. 11.
[Lyon](https://www.fotmob.com/ko/teams/9748/overview/lyon)[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)
[RWRayan Cherki](https://www.fotmob.com/ko/players/1104053/rayan-cherki)
€3650만
2025. 6. 11.
[Sunderland](https://www.fotmob.com/ko/teams/8472/overview/sunderland)[Dortmund](https://www.fotmob.com/ko/teams/9789/overview/dortmund)
[DMJobe Bellingham](https://www.fotmob.com/ko/players/1287373/jobe-bellingham)
€3060만
2025. 6. 11.
[Wolves](https://www.fotmob.com/ko/teams/8602/overview/wolves)[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)
[LWBRayan Ait Nouri](https://www.fotmob.com/ko/players/933845/rayan-ait-nouri)
€3680만
2025. 6. 10.
[Marseille](https://www.fotmob.com/ko/teams/8592/overview/marseille)[Inter](https://www.fotmob.com/ko/teams/8636/overview/inter)
[RWBLuis Henrique](https://www.fotmob.com/ko/players/1114635/luis-henrique)
밝혀지지 않음
2025. 6. 8.
[Nice](https://www.fotmob.com/ko/teams/9831/overview/nice)[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)
[CBJean-Clair Todibo](https://www.fotmob.com/ko/players/955214/jean-clair-todibo)
밝혀지지 않음
2025. 6. 7.
[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)[Juventus](https://www.fotmob.com/ko/teams/9885/overview/juventus)
[CBPierre Kalulu](https://www.fotmob.com/ko/players/1131217/pierre-kalulu)
€1450만
2025. 6. 6.
[Al Ahli](https://www.fotmob.com/ko/teams/2530/overview/al-ahli)[FC Porto](https://www.fotmob.com/ko/teams/9773/overview/fc-porto)
[AMGabriel Veiga](https://www.fotmob.com/ko/players/1116734/gabriel-veiga)
€1500만
2025. 6. 6.
[Arsenal](https://www.fotmob.com/ko/teams/9825/overview/arsenal)[Lazio](https://www.fotmob.com/ko/teams/8543/overview/lazio)
[LBNuno Tavares](https://www.fotmob.com/ko/players/957118/nuno-tavares)
€900만
2025. 6. 6.
[Ipswich](https://www.fotmob.com/ko/teams/9902/overview/ipswich)[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)
[STLiam Delap](https://www.fotmob.com/ko/players/1113903/liam-delap)
€3550만
2025. 6. 5.
[Roma](https://www.fotmob.com/ko/teams/8686/overview/roma)[Sunderland](https://www.fotmob.com/ko/teams/8472/overview/sunderland)
[DMEnzo Le Fee](https://www.fotmob.com/ko/players/1049999/enzo-le-fee)
€2300만
2025. 6. 4.
[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)[Brentford](https://www.fotmob.com/ko/teams/9937/overview/brentford)
[골키퍼Caoimhin Kelleher](https://www.fotmob.com/ko/players/776689/caoimhin-kelleher)
€2100만
2025. 6. 4.
[Sporting CP](https://www.fotmob.com/ko/teams/9768/overview/sporting-cp)[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)
[DMDario Essugo](https://www.fotmob.com/ko/players/1239595/dario-essugo)
€2227만
2025. 6. 3.
[Wolves](https://www.fotmob.com/ko/teams/8602/overview/wolves)[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)
[AMMatheus Cunha](https://www.fotmob.com/ko/players/863098/matheus-cunha)
€7400만
2025. 6. 2.
[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)
[RWBJeremie Frimpong](https://www.fotmob.com/ko/players/966018/jeremie-frimpong)
밝혀지지 않음
2025. 5. 31.
[Liverpool](https://www.fotmob.com/ko/teams/8650/overview/liverpool)[Real Madrid](https://www.fotmob.com/ko/teams/8633/overview/real-madrid)
[RBTrent Alexander-Arnold](https://www.fotmob.com/ko/players/760712/trent-alexander-arnold)
€1000만
2025. 5. 30.
[Fiorentina](https://www.fotmob.com/ko/teams/8535/overview/fiorentina)[Brentford](https://www.fotmob.com/ko/teams/9937/overview/brentford)
[RBMichael Kayode](https://www.fotmob.com/ko/players/1429912/michael-kayode)
€1770만
2025. 5. 30.
[Leverkusen](https://www.fotmob.com/ko/teams/8178/overview/leverkusen)[Bayern München](https://www.fotmob.com/ko/teams/9823/overview/bayern-munchen)
[CBJonathan Tah](https://www.fotmob.com/ko/players/469700/jonathan-tah)
자유 이적
2025. 5. 29.
[Bournemouth](https://www.fotmob.com/ko/teams/8678/overview/bournemouth)[Real Madrid](https://www.fotmob.com/ko/teams/8633/overview/real-madrid)
[CBDean Huijsen](https://www.fotmob.com/ko/players/1367619/dean-huijsen)
€5950만
2025. 5. 18.
[Barcelona](https://www.fotmob.com/ko/teams/8634/overview/barcelona)[Palmeiras](https://www.fotmob.com/ko/teams/10283/overview/palmeiras)
[STVitor Roque](https://www.fotmob.com/ko/players/1339347/vitor-roque)
€2550만
2025. 3. 1.
[Southampton](https://www.fotmob.com/ko/teams/8466/overview/southampton)[West Brom](https://www.fotmob.com/ko/teams/8659/overview/west-brom)
[STAdam Armstrong](https://www.fotmob.com/ko/players/519835/adam-armstrong)
임대
2025. 2. 5.
[Middlesbrough](https://www.fotmob.com/ko/teams/8549/overview/middlesbrough)[Atlanta United](https://www.fotmob.com/ko/teams/773958/overview/atlanta-united)
[STEmmanuel Latte Lath](https://www.fotmob.com/ko/players/783585/emmanuel-latte-lath)
€2125만
2025. 2. 5.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)
[CBAxel Disasi](https://www.fotmob.com/ko/players/696646/axel-disasi)
€600만. 임대 중
2025. 2. 4.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Crystal Palace](https://www.fotmob.com/ko/teams/9826/overview/crystal-palace)
[LBBen Chilwell](https://www.fotmob.com/ko/players/672469/ben-chilwell)
임대
2025. 2. 4.
[Chelsea](https://www.fotmob.com/ko/teams/8455/overview/chelsea)[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)
[LWJoao Félix](https://www.fotmob.com/ko/players/794427/joao-felix)
€550만. 임대 중
2025. 2. 4.
[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)[West Ham](https://www.fotmob.com/ko/teams/8654/overview/west-ham)
[STEvan Ferguson](https://www.fotmob.com/ko/players/1068482/evan-ferguson)
임대
2025. 2. 4.
[Bayern München](https://www.fotmob.com/ko/teams/9823/overview/bayern-munchen)[Tottenham](https://www.fotmob.com/ko/teams/8586/overview/tottenham)
[LWMathys Tel](https://www.fotmob.com/ko/players/1288111/mathys-tel)
임대
2025. 2. 4.
[Juventus](https://www.fotmob.com/ko/teams/9885/overview/juventus)[Fiorentina](https://www.fotmob.com/ko/teams/8535/overview/fiorentina)
[CMNicolo Fagioli](https://www.fotmob.com/ko/players/951712/nicolo-fagioli)
임대
2025. 2. 4.
[FC Porto](https://www.fotmob.com/ko/teams/9773/overview/fc-porto)[Man City](https://www.fotmob.com/ko/teams/8456/overview/man-city)
[DMNico González](https://www.fotmob.com/ko/players/1280132/nico-gonzalez)
€6000만
2025. 2. 4.
[PSG](https://www.fotmob.com/ko/teams/9847/overview/psg)[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)
[STMarco Asensio](https://www.fotmob.com/ko/players/498033/marco-asensio)
임대
2025. 2. 4.
[Feyenoord](https://www.fotmob.com/ko/teams/10235/overview/feyenoord)[Milan](https://www.fotmob.com/ko/teams/8564/overview/milan)
[STSantiago Gimenez](https://www.fotmob.com/ko/players/954092/santiago-gimenez)
€3200만
2025. 2. 4.
[1. FC Nürnberg](https://www.fotmob.com/ko/teams/8165/overview/1-fc-nurnberg)[Brighton](https://www.fotmob.com/ko/teams/10204/overview/brighton)
[STStefanos Tzimas](https://www.fotmob.com/ko/players/1423616/stefanos-tzimas)
€2500만
2025. 2. 3.
[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)[Aston Villa](https://www.fotmob.com/ko/teams/10252/overview/aston-villa)
[LWMarcus Rashford](https://www.fotmob.com/ko/players/696365/marcus-rashford)
임대
2025. 2. 3.
[Rennes](https://www.fotmob.com/ko/teams/9851/overview/rennes)[Frankfurt](https://www.fotmob.com/ko/teams/9810/overview/frankfurt)
[CBArthur Theate](https://www.fotmob.com/ko/players/1173250/arthur-theate)
€1310만
2025. 2. 3.
[Lecce](https://www.fotmob.com/ko/teams/9888/overview/lecce)[Man United](https://www.fotmob.com/ko/teams/10260/overview/man-united)
[LBPatrick Dorgu](https://www.fotmob.com/ko/players/1526560/patrick-dorgu)
€3000만
2025. 2. 3.
"""

# Map club name standardizations
CLUB_MAP = {
    "Tottenham": "Tottenham Hotspur",
    "Man City": "Manchester City",
    "Man United": "Manchester United",
    "Chelsea": "Chelsea",
    "Arsenal": "Arsenal",
    "Liverpool": "Liverpool",
    "Aston Villa": "Aston Villa",
    "Newcastle": "Newcastle United",
    "Real Madrid": "Real Madrid",
    "Barcelona": "FC Barcelona",
    "Atletico Madrid": "Atlético Madrid",
    "Bayern München": "Bayern Munich",
    "Dortmund": "Borussia Dortmund",
    "Milan": "AC Milan",
    "Inter": "Inter Milan",
    "Juventus": "Juventus",
    "PSG": "Paris Saint-Germain",
    "Marseille": "Olympique de Marseille",
    "Lyon": "Olympique Lyonnais",
    "Monaco": "AS Monaco",
    "Leverkusen": "Bayer 04 Leverkusen",
    "RB Leipzig": "RB Leipzig",
    "Sporting CP": "Sporting CP",
    "Benfica": "Benfica",
    "FC Porto": "FC Porto",
    "Ajax": "Ajax",
    "Feyenoord": "Feyenoord",
    "Al Hilal": "Al Hilal",
    "Al Nassr FC": "Al Nassr",
    "Al Ittihad": "Al Ittihad",
    "Al Ahli": "Al Ahli",
    "Inter Miami CF": "Inter Miami",
    "Galatasaray": "Galatasaray",
    "Fenerbahçe": "Fenerbahçe",
    "Beşiktaş": "Beşiktaş",
    "Trabzonspor": "Trabzonspor",
    "Como": "Como 1907",
    "Atalanta": "Atalanta BC",
    "Napoli": "SSC Napoli",
    "Roma": "AS Roma",
    "Lazio": "SS Lazio",
    "Fiorentina": "Fiorentina",
    "Villarreal": "Villarreal CF",
    "Real Sociedad": "Real Sociedad",
    "Real Betis": "Real Betis",
    "Sevilla": "Sevilla FC",
    "Crystal Palace": "Crystal Palace",
    "Everton": "Everton",
    "West Ham": "West Ham United",
    "Wolves": "Wolverhampton Wanderers",
    "Brighton": "Brighton & Hove Albion",
    "Fulham": "Fulham",
    "Brentford": "Brentford",
    "Bournemouth": "AFC Bournemouth",
    "Nottm Forest": "Nottingham Forest",
    "Sunderland": "Sunderland",
    "Leeds": "Leeds United",
    "Burnley": "Burnley",
    "Strasbourg": "RC Strasbourg",
    "Rennes": "Stade Rennais",
    "Nice": "OGC Nice",
    "Lens": "RC Lens",
    "Frankfurt": "Eintracht Frankfurt",
    "VfB Stuttgart": "VfB Stuttgart",
    "Wolfsburg": "VfL Wolfsburg",
}

LEAGUE_MAP = {
    "Tottenham Hotspur": ("Premier League", 1),
    "Manchester City": ("Premier League", 1),
    "Manchester United": ("Premier League", 1),
    "Chelsea": ("Premier League", 1),
    "Arsenal": ("Premier League", 1),
    "Liverpool": ("Premier League", 1),
    "Aston Villa": ("Premier League", 1),
    "Newcastle United": ("Premier League", 1),
    "Crystal Palace": ("Premier League", 1),
    "Everton": ("Premier League", 1),
    "West Ham United": ("Premier League", 1),
    "Wolverhampton Wanderers": ("Premier League", 1),
    "Brighton & Hove Albion": ("Premier League", 1),
    "Fulham": ("Premier League", 1),
    "Brentford": ("Premier League", 1),
    "AFC Bournemouth": ("Premier League", 1),
    "Nottingham Forest": ("Premier League", 1),
    "Sunderland": ("Premier League", 1),
    "Leeds United": ("Championship", 2),
    "Burnley": ("Championship", 2),
    "Real Madrid": ("La Liga", 1),
    "FC Barcelona": ("La Liga", 1),
    "Atlético Madrid": ("La Liga", 1),
    "Villarreal CF": ("La Liga", 1),
    "Real Sociedad": ("La Liga", 1),
    "Real Betis": ("La Liga", 1),
    "Sevilla FC": ("La Liga", 1),
    "Girona": ("La Liga", 1),
    "Valencia": ("La Liga", 1),
    "Bayern Munich": ("Bundesliga", 1),
    "Borussia Dortmund": ("Bundesliga", 1),
    "Bayer 04 Leverkusen": ("Bundesliga", 1),
    "RB Leipzig": ("Bundesliga", 1),
    "Eintracht Frankfurt": ("Bundesliga", 1),
    "VfB Stuttgart": ("Bundesliga", 1),
    "VfL Wolfsburg": ("Bundesliga", 1),
    "AC Milan": ("Serie A", 1),
    "Inter Milan": ("Serie A", 1),
    "Juventus": ("Serie A", 1),
    "SSC Napoli": ("Serie A", 1),
    "AS Roma": ("Serie A", 1),
    "SS Lazio": ("Serie A", 1),
    "Atalanta BC": ("Serie A", 1),
    "Fiorentina": ("Serie A", 1),
    "Como 1907": ("Serie A", 1),
    "Paris Saint-Germain": ("Ligue 1", 1),
    "Olympique de Marseille": ("Ligue 1", 1),
    "Olympique Lyonnais": ("Ligue 1", 1),
    "AS Monaco": ("Ligue 1", 1),
    "Stade Rennais": ("Ligue 1", 1),
    "OGC Nice": ("Ligue 1", 1),
    "RC Lens": ("Ligue 1", 1),
    "RC Strasbourg": ("Ligue 1", 1),
    "Sporting CP": ("Liga Portugal", 1),
    "Benfica": ("Liga Portugal", 1),
    "FC Porto": ("Liga Portugal", 1),
    "Ajax": ("Eredivisie", 1),
    "Feyenoord": ("Eredivisie", 1),
    "Al Hilal": ("Saudi Pro League", 1),
    "Al Nassr": ("Saudi Pro League", 1),
    "Al Ittihad": ("Saudi Pro League", 1),
    "Al Ahli": ("Saudi Pro League", 1),
    "Al Qadsiah": ("Saudi Pro League", 1),
    "Inter Miami": ("MLS", 1),
    "Galatasaray": ("Süper Lig", 1),
    "Fenerbahçe": ("Süper Lig", 1),
    "Beşiktaş": ("Süper Lig", 1),
    "Trabzonspor": ("Süper Lig", 1),
}

def parse_entries(text):
    # Regex pattern to match FotMob transfer blocks:
    # Pattern format:
    # [FromClub](...)[ToClub](...) OR Free agent[ToClub](...) OR [FromClub](...)Free agent
    # [PosPlayerName](https://...)
    # Fee or type
    # Date
    
    # Split text into lines
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    
    transfers = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if line contains player link
        player_match = re.search(r'\[(?:[A-Z]{1,3}|골키퍼)?([A-Za-z0-9\s\.\'\-äöüéèêàáíóúñçãõøÅåØæÆ]+)\]\(https://www\.fotmob\.com/ko/players/(\d+)/([^\)]+)\)', line)
        if player_match:
            player_name = player_match.group(1).strip()
            fotmob_id = player_match.group(2).strip()
            slug = player_match.group(3).strip()
            
            # Previous line or 2 lines above is club info
            club_line = lines[i-1] if i > 0 else ""
            if "overview" not in club_line and "Free agent" not in club_line and i > 1:
                club_line = lines[i-2] + " " + lines[i-1]
                
            # Next lines have fee and date
            fee_line = lines[i+1] if i+1 < len(lines) else ""
            date_line = lines[i+2] if i+2 < len(lines) else ""
            
            # Parse ToClub
            # Examples: [Milan](...)[Bournemouth](...) -> to Bournemouth
            # Free agent[Feyenoord](...) -> to Feyenoord
            # [Torino](...)Free agent -> to Free agent
            to_club = None
            from_club = None
            
            clubs = re.findall(r'\[([^\]]+)\]\(https://www\.fotmob\.com/ko/teams/[^\)]+\)', club_line)
            if len(clubs) >= 2:
                from_club = clubs[0]
                to_club = clubs[1]
            elif len(clubs) == 1:
                if "Free agent" in club_line:
                    if club_line.startswith("Free agent") or "Free agent[" in club_line:
                        from_club = "Free agent"
                        to_club = clubs[0]
                    else:
                        from_club = clubs[0]
                        to_club = "Free agent"
                elif "Neom SC" in club_line:
                    if "Neom SC[" in club_line or club_line.startswith("Neom SC"):
                        from_club = "Neom SC"
                        to_club = clubs[0]
                    else:
                        from_club = clubs[0]
                        to_club = "Neom SC"
                elif "Al Qadasiya" in club_line or "Al-Diraiyah" in club_line or "Qatar SC" in club_line:
                    to_club = clubs[0]
                else:
                    to_club = clubs[0]
            
            # Fee parsing
            val_eur = 25.0
            if "자유 이적" in fee_line or "자유" in fee_line:
                fee_type = "Free"
            elif "임대" in fee_line:
                fee_type = "Loan"
            else:
                fee_type = "Transfer"
                # e.g. €1850만 -> 18.5M, €1.4억 -> 140M, €6360만 -> 63.6M, €500만 -> 5.0M
                m_eur = re.search(r'€([\d\.]+)억', fee_line)
                if m_eur:
                    val_eur = float(m_eur.group(1)) * 100.0
                else:
                    m_man = re.search(r'€([\d\.]+)만', fee_line)
                    if m_man:
                        val_eur = float(m_man.group(1)) / 100.0

            if to_club:
                clean_to_club = CLUB_MAP.get(to_club, to_club)
                league_info = LEAGUE_MAP.get(clean_to_club, ("Global League", 1))
                transfers.append({
                    "player_name": player_name,
                    "slug": slug,
                    "fotmob_id": fotmob_id,
                    "from_club": from_club,
                    "to_club": clean_to_club,
                    "fee_type": fee_type,
                    "val_eur": val_eur,
                    "league": league_info[0],
                    "tier": league_info[1],
                    "date": date_line
                })
        i += 1
    return transfers

def apply_all():
    transfers = parse_entries(RAW_TEXT)
    print(f"Parsed {len(transfers)} transfer items from raw text.")
    
    conn = sqlite3.connect(r"c:\Users\MJ\Desktop\football scout AI\backend\data\scout_hub.sqlite")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    updated_count = 0
    not_found = []
    
    # Process each transfer
    for t in transfers:
        name = t["player_name"]
        slug_name = t["slug"].replace("-", " ")
        to_club = t["to_club"]
        val = t["val_eur"]
        league = t["league"]
        tier = t["tier"]
        
        # Don't overwrite if to_club is Free agent unless intentional, but set club to to_club
        c.execute("""
        UPDATE players
        SET club = ?, market_value_eur = CASE WHEN ? > 1.0 THEN ? ELSE market_value_eur END, league = ?, league_tier = ?
        WHERE full_name LIKE ? OR name LIKE ? OR id LIKE ?
        """, (to_club, val, val, league, tier, f"%{name}%", f"%{name}%", f"%{t['slug']}%"))
        
        if c.rowcount > 0:
            updated_count += c.rowcount
            # print(f"Updated {name} -> {to_club} (count={c.rowcount})")
        else:
            not_found.append(t)
            
    conn.commit()
    conn.close()
    print(f"Successfully applied {updated_count} player updates to DB.")
    print(f"{len(not_found)} transfers were not already present in the DB (can be added if major).")
    for nf in not_found[:15]:
        print(f"  - {nf['player_name']} ({nf['slug']}) -> {nf['to_club']}")

if __name__ == "__main__":
    apply_all()
