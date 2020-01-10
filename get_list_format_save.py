import json
import requests


drug_list = ["4-meo-mipt","5-eapb","2-fma","morphine","5-apdb","atomoxetine","medazepam","5-br-dmt","sufentanil","ald-52","methoxyacetyl-fentanyl","5-it","buprenorphine","deschloroetizolam","methaqualone","a-pvp","pagoclone","5-meo-dipt","cyclobenzaprine","3-fma","4,4-dmar","doc","theacrine","hydromorphone","nicomorphine","2c-b-an","moclobemide","6-mapb","4-ho-mcpt","25ip-nbome","salvia","pre-084","doxylamine","bentazepam","1b-lsd","methallylescaline","hexobarbital","2c-e","secobarbital","2-pa","ethyl-pentedrone","oxazepam","hot-2","lormetazepam","nefiracetam","methylphenidate","dalt","25t-4-nbome","cloniprazepam","2c-g","6-apdb","flualprazolam","dopr","25t-2-nbome","1,4-butanediol","5-meo-dmt","4-ho-ept","methamphetamine","fluorolintane","diphenidine","4-meo-pcp","4-benzylpiperidine","2c-t-21","butyrfentanyl","fluclotizolam","4-fa","clobazam","dibutylone","aleph","bromazolam","3-meo-pcpr","vyvanse","tma-2","4-fluoropentedrone","3-meo-pcpy","quetiapine","5-methyl-bk-mdea","tiletamine","methylone","lsa","4-ho-mpt","tramadol","2c-t","ethketamine","furanylfentanyl","2c-n","escaline","4-fluoromethylphenidate","mdma","buphedrone","hydrocodone","2-chloro-ephenidine","ethylphenidate","barbital","mushrooms","cocaine","mt-45","alpha-php","4-mta","3-meo-pcp","dom","mebroqualone","5-meo-dalt","dexedrine","flubromazepam","25c-nbome","jenkem","ketazolam","diethyl-ether","3-fa","cyclopentyl-fentanyl","25i-nbf","mda","bk-2c-b","25e-nbome","dextropropoxyphene","flurazepam","amfecloral","3c-e","2c-b","aspirin","gaba","25i-nbome","mbdb","trazodone","tetrahydrofuran-fentanyl","pentazocine","prolintane","methylmethaqualone","βh-2c-b","o-pce","4-methylaminorex","25n-nbome","3-mec","methedrone","naphyrone","4-aco-mipt","adrafinil","4-ho-det","clonazolam","methadone","4-mec","nitrous","memantine","4f-pvp","eth-lad","isopropylphenidate","5-htp","gbl","mdpv","focalin","hdep-28","mexazolam","pseudoephedrine","mephtetramine","dihydrocodeine","25d-nbome","ethylcathinone","4-meo-butryfentanyl","ghb","doi","allobarbital","4-emc","scopolamine","homosildenafil","carisoprodol","acetildenafil","rti-111","mcpp","pma","clonitazene","4-ho-mipt","bk-ivp","clomethiazole","sulbutiamine","ept","g-130","phenethylamine","3-fmc","mpa","25i-nbmd","ab-fubinaca","baclofen","butylone","amfonelicacid","pramiracetam","5-meo-dpt","2c-t-7","psilocin","rilmazafone","methoxypiperamide","kava","pipt","propofol","alcohol","glutethimide","lsz","4f-php","pinazepam","bzp","crl-40-941","flubromazolam","4-fpm","5-mapdb","3-ho-pce","ethylone","amt","dph","metaxalone","mephedrone","glaucine","mdphp","crl-40-940","mk-801","mexamine","citalopram","25g-nbome","clonidine","dipipanone","ephenidine","th-pvp","propylhexedrine","2c-t-2","fluorophenibut","dipt","benzydamine","nimetazepam","pst","bromazepam","d2pm","lsm-775","pentobarbital","cannabis","viagra","5-meo-amt","u-47700","parafluorobutyrfentanyl","2-mec","rolicyclidine","nicotine","5-dbfpv","2-methyl-2-butanol","amphetamine","pcp","2c-b-fly","tetrazepam","pce","pv-9","3-cmc","apap","noctec","librium","4-aco-det","kanna","25p-nbome","prl-8-53","pemoline","quazepam","pentylone","doet","dpt","zolazepam","pyrophenidone","halazepam","khat","4-ho-mpmi","25h-nbome","5-meo-met","pentedrone","a-pvt","ibogaine","chloral-betaine","flutoprazepam","acetylfentanyl","nitemazepam","phenazepam","isophenmetrazine","aet","3-meo-pcmo","kratom","etizolam","bk-2c-i","peyote","mem","mxm","noopept","marinol","5-bpdi","5-apb","dramamine","2c-p","ayahuasca","picamilon","4-ho-dipt","adderall","temazepam","bupropion","dimemebfe","4-fmc","piracetam","tolibut","6-apb","centrophenoxine","dob","methylmorphenate","5-ppdi","demerol","methoxphenidine","3-mmc","parafluorofentanyl","cloxazolam","4-aco-dalt","dmaa","5-meo-pyr-t","db-mdbp","changa","promethazine","nitrazepam","2-pta","methamnetamine","morpheridine","4f-neb","caffeine","acryl-fentanyl","aleph-2","methyprylon","melatonin","nm-2-ai","fentanyl","gabapentin","amobarbital","5-meo-mipt","metizolam","bod","2-ai","6-mddm","propylphenidate","2-fdck","mxe","3-oh-phenazepam","ephedrine","opium","4-ho-dpt","25b-nboh","oxazolam","naproxen","det","cialis","midazolam","ah-7921","truffles","yerba-mate","hexedrone","α-pbp","don","3c-p","c30-nbome","4-aco-dmt","nifoxipam","5-iai","afloqualone","norflurazepam","2-fea","4-aco-dpt","25i-nboh","u-51754","hydroxyzine","bromo-dragonfly","troparil","phenobarbital","thiopental","flunitrazepam","brotizolam","4-methylmethylphenidate","pyrazolam","3,6-dmpm","diclazepam","4-mpd","phenmetrazine","pfbt","oxycodone","sonata","2-nmc","clorazepate","datura","mephenmetrazine","2-me-dmt","mdoh","5-mapb","bromadol","loprazolam","carphedon","delorazepam","aniracetam","diclofensine","doip","neb","proscaline","pro-lad","ethaqualone","3-meomc","viloxazine","am-2201","diazepam","4-aco-dipt","3-fea","4-fpp","adinazolam","nitrazolam","2c-t-4","clonazepam","ronlax","phentermine","indapyrophenidone","bromantane","5-meo-dibf","4-ho-met","2-dpmp","tilidine","placdyl","ketobemidone","triazolam","thiopropamine","lorazepam","nitracaine","3,4-ctmp","ashwagandha","3-meo-pce","4-epd","4-aco-met","propranolol","2c-c","isomethadone","hexen","codeine","dmt","alprazolam","oxymorphone","2-mppp","3-ho-pcp","o-desmethyltramadol","4-chlorodiazepam","tapentadol","desmethylflunitrazepam","chloroform","ibuprofen","palfium","isoproscaline","hdmp-28","25c-nboh","allylescaline","2-methylamphetamine","mdea","mbzp","5f-akb48","1p-lsd","1p-eth-lad","1cp-lsd","mescaline","lsd","estazolam","5-meo-malt","halothane","dxm","5-meo-nipt","tma-6","u-49900","4-cic","2c-d","coronaridine","benzodioxole-fentanyl","coluracetam","modafinil","cyclo-methiodrone","zopiclone","mexedrone","flutazolam","a-pihp","phenibut","pv-10","aminorex","4-fma","l-theanine","25b-nbome","armodafinil","huperzine-a","mdpa","pv-8","mipt","clotiazepam","homomazindol","nordazepam","valerylfentanyl","met","aminotadalafil","eszopiclone","sinicuichi","2c-ip","w-15","6-eapb","ab-chminaca","2c-i","pregabalin","2-fa","4-cbc","4-cmc","2-mmc","5-apdi","cinolazepam","meclonazepam","cyclopropylmescaline","flunitrazolam","tuinal","oxiracetam","4-cma","dehydroxyfluorafinil","zolpidem","deschloroketamine","prazepam","5-meo-eipt","2c-b-fly-nbome","heroin","tianeptine","al-lad","hot-7","methoxyketamine","propoxyphene","3-fpm","metaclazepam","ketamine","mdai","phenetrazine","dimethylone","4-fea","eflea","yopo","camazepam","ethylmorphine","fasoracetam","5f-pb-22","4-fluoroethylphenidate","cyclizine","indapex"]
result = []
for drug in drug_list:
    params = {'name': drug}
    raw = requests.get('http://tripbot.tripsit.me/api/tripsit/getDrug', params=params).json()
    if raw['err'] is None:
        pretty_name = raw['data'][0]['pretty_name']
        try:
            aliases = raw['data'][0]['aliases']
            for name in aliases:
                result.append(name)
        except:
            pass
        result.append(pretty_name)

with open('drug_list.txt', 'w') as outfile:
    json.dump(result, outfile)



# result = []
# for i in range(1, 999):
#     result.append(str(i))
# with open('dose_list.txt', 'w') as outfile:
#     json.dump(result, outfile)



# μg
# unit_str = "ug, mg, g, kg, mL, L, fl oz"
# result = []
# for unit in unit_str.split(','):
#     result.append(unit)
# with open('unit_list.txt', 'w') as outfile:
#     json.dump(result, outfile)