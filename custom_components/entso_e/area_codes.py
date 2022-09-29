"""Area Codes for Entso-e integration."""

# BZN — Bidding Zone
# BZA — Bidding Zone Aggregation
# CA — Control Area
# MBA — Market Balance Area
# IBA — Imbalance Area 
# IPA — Imbalance Price Area 
# LFA — Load Frequency Control Area 
# LFB — Load Frequency Control Block
# REG — Region
# SCA — Scheduling Area
# SNA — Synchronous Area

area_codes = [
{'code': '10Y1001A1001A016',  'desc': 'CTA|NIE, MBA|SEM(SONI), SCA|NIE'},
{'code': '10Y1001A1001A39I',  'desc': 'SCA|EE, MBA|EE, CTA|EE, BZN|EE, Estonia (EE)', 'area': 'EE'},
{'code': '10Y1001A1001A44P',  'desc': 'IPA|SE1, BZN|SE1, MBA|SE1, SCA|SE1', 'area': 'SE1'},
{'code': '10Y1001A1001A45N',  'desc': 'SCA|SE2, MBA|SE2, BZN|SE2, IPA|SE2', 'area': 'SE2'},
{'code': '10Y1001A1001A46L',  'desc': 'IPA|SE3, BZN|SE3, MBA|SE3, SCA|SE3', 'area': 'SE3'},
{'code': '10Y1001A1001A47J',  'desc': 'SCA|SE4, MBA|SE4, BZN|SE4, IPA|SE4', 'area': 'SE4'},
{'code': '10Y1001A1001A48H',  'desc': 'IPA|NO5, IBA|NO5, BZN|NO5, MBA|NO5, SCA|NO5', 'area': 'NO5'},
{'code': '10Y1001A1001A49F',  'desc': 'SCA|RU, MBA|RU, BZN|RU, CTA|RU', 'area': 'RU'},
{'code': '10Y1001A1001A50U',  'desc': 'CTA|RU-KGD, BZN|RU-KGD, MBA|RU-KGD, SCA|RU-KGD', 'area': 'RU-KGD'},
{'code': '10Y1001A1001A51S',  'desc': 'SCA|BY, MBA|BY, BZN|BY, CTA|BY'},
{'code': '10Y1001A1001A59C',  'desc': 'BZN|IE(SEM), MBA|IE(SEM), SCA|IE(SEM), LFB|IE-NIE, SNA|Ireland', 'area': 'IE(SEM)'},
{'code': '10Y1001A1001A63L',  'desc': 'BZN|DE-AT-LU', 'area': 'DE-AT-LU'},
{'code': '10Y1001A1001A64J',  'desc': 'BZN|NO1A', 'area': 'NO1A'},
{'code': '10Y1001A1001A65H',  'desc': 'Denmark (DK)'},
{'code': '10Y1001A1001A66F',  'desc': 'BZN|IT-GR', 'area': 'IT-GR'},
{'code': '10Y1001A1001A67D',  'desc': 'BZN|IT-North-SI', 'area': 'IT-North-SI'},
{'code': '10Y1001A1001A68B',  'desc': 'BZN|IT-North-CH', 'area': 'IT-North-CH'},
{'code': '10Y1001A1001A699',  'desc': 'BZN|IT-Brindisi, SCA|IT-Brindisi, MBA|IT-Z-Brindisi', 'area': 'IT-Brindisi'},
{'code': '10Y1001A1001A70O',  'desc': 'MBA|IT-Z-Centre-North, SCA|IT-Centre-North, BZN|IT-Centre-North', 'area': 'IT-Centre-North'},
{'code': '10Y1001A1001A71M',  'desc': 'BZN|IT-Centre-South, SCA|IT-Centre-South, MBA|IT-Z-Centre-South', 'area': 'IT-Centre-South'},
{'code': '10Y1001A1001A72K',  'desc': 'MBA|IT-Z-Foggia, SCA|IT-Foggia, BZN|IT-Foggia', 'area': 'IT-Foggia'},
{'code': '10Y1001A1001A73I',  'desc': 'BZN|IT-North, SCA|IT-North, MBA|IT-Z-North', 'area': 'IT-North'},
{'code': '10Y1001A1001A74G',  'desc': 'MBA|IT-Z-Sardinia, SCA|IT-Sardinia, BZN|IT-Sardinia', 'area': 'IT-Sardinia'},
{'code': '10Y1001A1001A75E',  'desc': 'BZN|IT-Sicily, SCA|IT-Sicily, MBA|IT-Z-Sicily', 'area': 'IT-Sicily'},
{'code': '10Y1001A1001A76C',  'desc': 'MBA|IT-Z-Priolo, SCA|IT-Priolo, BZN|IT-Priolo', 'area': 'IT-Priolo'},
{'code': '10Y1001A1001A77A',  'desc': 'BZN|IT-Rossano, SCA|IT-Rossano, MBA|IT-Z-Rossano', 'area': 'IT-Rossano'},
{'code': '10Y1001A1001A788',  'desc': 'MBA|IT-Z-South, SCA|IT-South, BZN|IT-South', 'area': 'IT-South'},
{'code': '10Y1001A1001A796',  'desc': 'CTA|DK'},
{'code': '10Y1001A1001A80L',  'desc': 'BZN|IT-North-AT', 'area': 'IT-North-AT'},
{'code': '10Y1001A1001A81J',  'desc': 'BZN|IT-North-FR', 'area': 'IT-North-FR'},
{'code': '10Y1001A1001A82H',  'desc': 'BZN|DE-LU, IPA|DE-LU, SCA|DE-LU, MBA|DE-LU', 'area': 'DE-LU'},
{'code': '10Y1001A1001A83F',  'desc': 'Germany (DE)'},
{'code': '10Y1001A1001A84D',  'desc': 'MBA|IT-MACRZONENORTH, SCA|IT-MACRZONENORTH'},
{'code': '10Y1001A1001A85B',  'desc': 'SCA|IT-MACRZONESOUTH, MBA|IT-MACRZONESOUTH'},
{'code': '10Y1001A1001A869',  'desc': 'SCA|UA-DobTPP, BZN|UA-DobTPP, CTA|UA-DobTPP', 'area': 'UA-DobTPP'},
{'code': '10Y1001A1001A877',  'desc': 'BZN|IT-Malta', 'area': 'IT-Malta'},
{'code': '10Y1001A1001A885',  'desc': 'BZN|IT-SACOAC', 'area': 'IT-SACOA'},
{'code': '10Y1001A1001A893',  'desc': 'BZN|IT-SACODC, SCA|IT-SACODC', 'area': 'IT-SACODC'},
{'code': '10Y1001A1001A91G',  'desc': 'SNA|Nordic, REG|Nordic, LFB|Nordic'},
{'code': '10Y1001A1001A92E',  'desc': 'United Kingdom (UK)'},
{'code': '10Y1001A1001A93C',  'desc': 'Malta (MT), BZN|MT, CTA|MT, SCA|MT, MBA|MT', 'area': 'MT'},
{'code': '10Y1001A1001A990',  'desc': 'MBA|MD, SCA|MD, CTA|MD, BZN|MD, Moldova (MD)', 'area': 'MD'},
{'code': '10Y1001A1001B004',  'desc': 'Armenia (AM), BZN|AM, CTA|AM', 'area': 'AM'},
{'code': '10Y1001A1001B012',  'desc': 'CTA|GE, BZN|GE, Georgia (GE), SCA|GE, MBA|GE', 'area': 'GE'},
{'code': '10Y1001A1001B05V',  'desc': 'Azerbaijan (AZ), BZN|AZ, CTA|AZ', 'area': 'AZ'},
{'code': '10Y1001C--00003F',  'desc': 'BZN|UA, Ukraine (UA), MBA|UA, SCA|UA', 'area': 'UA'},
{'code': '10Y1001C--000182',  'desc': 'SCA|UA-IPS, MBA|UA-IPS, BZN|UA-IPS, CTA|UA-IPS', 'area': 'UA-IPS'},
{'code': '10Y1001C--00038X',  'desc': 'BZA|CZ-DE-SK-LT-SE4'},
{'code': '10Y1001C--00059P',  'desc': 'REG|CORE'},
{'code': '10Y1001C--00090V',  'desc': 'REG|AFRR, SCA|AFRR'},
{'code': '10Y1001C--00095L',  'desc': 'REG|SWE'},
{'code': '10Y1001C--00096J',  'desc': 'SCA|IT-Calabria, MBA|IT-Z-Calabria, BZN|IT-Calabria', 'area': 'IT-Calabria'},
{'code': '10Y1001C--00098F',  'desc': 'BZN|GB(IFA)', 'area': 'GB(IFA)'},
{'code': '10Y1001C--00100H',  'desc': 'BZN|XK, CTA|XK, Kosovo (XK), MBA|XK, LFB|XK, LFA|XK', 'area': 'XK'},
{'code': '10Y1001C--00119X',  'desc': 'SCA|IN'},
{'code': '10Y1001C--001219',  'desc': 'BZN|NO2A', 'area': 'NO2A'},
{'code': '10Y1001C--00137V',  'desc': 'REG|ITALYNORTH'},
{'code': '10Y1001C--00138T',  'desc': 'REG|GRIT'},
{'code': '10YAL-KESH-----5',  'desc': 'LFB|AL, LFA|AL, BZN|AL, CTA|AL, Albania (AL), SCA|AL, MBA|AL', 'area': 'AL'},
{'code': '10YAT-APG------L',  'desc': 'MBA|AT, SCA|AT, Austria (AT), IPA|AT, CTA|AT, BZN|AT, LFA|AT, LFB|AT', 'area': 'AT'},
{'code': '10YBA-JPCC-----D',  'desc': 'LFA|BA, BZN|BA, CTA|BA, Bosnia and Herz. (BA), SCA|BA, MBA|BA', 'area': 'BA'},
{'code': '10YBE----------2',  'desc': 'MBA|BE, SCA|BE, Belgium (BE), CTA|BE, BZN|BE, LFA|BE, LFB|BE', 'area': 'BE'},
{'code': '10YCA-BULGARIA-R',  'desc': 'LFB|BG, LFA|BG, BZN|BG, CTA|BG, Bulgaria (BG), SCA|BG, MBA|BG', 'area': 'BG'},
{'code': '10YCB-GERMANY--8',  'desc': 'SCA|DE_DK1_LU, LFB|DE_DK1_LU'},
{'code': '10YCB-JIEL-----9',  'desc': 'LFB|RS_MK_ME'},
{'code': '10YCB-POLAND---Z',  'desc': 'LFB|PL'},
{'code': '10YCB-SI-HR-BA-3',  'desc': 'LFB|SI_HR_BA'},
{'code': '10YCH-SWISSGRIDZ',  'desc': 'LFB|CH, LFA|CH, SCA|CH, MBA|CH, Switzerland (CH), CTA|CH, BZN|CH', 'area': 'CH'},
{'code': '10YCS-CG-TSO---S',  'desc': 'BZN|ME, CTA|ME, Montenegro (ME), MBA|ME, SCA|ME, LFA|ME', 'area': 'ME'},
{'code': '10YCS-SERBIATSOV',  'desc': 'LFA|RS, SCA|RS, MBA|RS, Serbia (RS), CTA|RS, BZN|RS', 'area': 'RS'},
{'code': '10YCY-1001A0003J',  'desc': 'BZN|CY, CTA|CY, Cyprus (CY), MBA|CY, SCA|CY', 'area': 'CY'},
{'code': '10YCZ-CEPS-----N',  'desc': 'SCA|CZ, MBA|CZ, Czech Republic (CZ), CTA|CZ, BZN|CZ, LFA|CZ, LFB|CZ', 'area': 'CZ'},
{'code': '10YDE-ENBW-----N',  'desc': 'LFA|DE(TransnetBW), CTA|DE(TransnetBW), SCA|DE(TransnetBW)'},
{'code': '10YDE-EON------1',  'desc': 'SCA|DE(TenneT GER), CTA|DE(TenneT GER), LFA|DE(TenneT GER)'},
{'code': '10YDE-RWENET---I',  'desc': 'LFA|DE(Amprion), CTA|DE(Amprion), SCA|DE(Amprion)'},
{'code': '10YDE-VE-------2',  'desc': 'SCA|DE(50Hertz), CTA|DE(50Hertz), LFA|DE(50Hertz), BZA|DE(50HzT)'},
{'code': '10YDK-1-------AA',  'desc': 'BZN|DK1A', 'area': 'DK1A'},
{'code': '10YDK-1--------W',  'desc': 'IPA|DK1, IBA|DK1, BZN|DK1, SCA|DK1, MBA|DK1, LFA|DK1', 'area': 'DK1'},
{'code': '10YDK-2--------M',  'desc': 'LFA|DK2, MBA|DK2, SCA|DK2, IBA|DK2, IPA|DK2, BZN|DK2', 'area': 'DK2'},
{'code': '10YDOM-1001A082L',  'desc': 'CTA|PL-CZ, BZA|PL-CZ'},
{'code': '10YDOM-CZ-DE-SKK',  'desc': 'BZA|CZ-DE-SK, BZN|CZ+DE+SK', 'area': 'CZ+DE+SK'},
{'code': '10YDOM-PL-SE-LT2',  'desc': 'BZA|LT-SE4'},
{'code': '10YDOM-REGION-1V',  'desc': 'REG|CWE'},
{'code': '10YES-REE------0',  'desc': 'LFB|ES, LFA|ES, BZN|ES, Spain (ES), CTA|ES, SCA|ES, MBA|ES', 'area': 'ES'},
{'code': '10YEU-CONT-SYNC0',  'desc': 'SNA|Continental Europe'},
{'code': '10YFI-1--------U',  'desc': 'MBA|FI, SCA|FI, CTA|FI, Finland (FI), BZN|FI, IPA|FI, IBA|FI', 'area': 'FI'},
{'code': '10YFR-RTE------C',  'desc': 'BZN|FR, France (FR), CTA|FR, SCA|FR, MBA|FR, LFB|FR, LFA|FR', 'area': 'FR'},
{'code': '10YGB----------A',  'desc': 'LFA|GB, LFB|GB, SNA|GB, MBA|GB, SCA|GB, CTA|National Grid, BZN|GB'},
{'code': '10YGR-HTSO-----Y',  'desc': 'BZN|GR, Greece (GR), CTA|GR, SCA|GR, MBA|GR, LFB|GR, LFA|GR', 'area': 'GR'},
{'code': '10YHR-HEP------M',  'desc': 'LFA|HR, MBA|HR, SCA|HR, CTA|HR, Croatia (HR), BZN|HR', 'area': 'HR'},
{'code': '10YHU-MAVIR----U',  'desc': 'BZN|HU, Hungary (HU), CTA|HU, SCA|HU, MBA|HU, LFA|HU, LFB|HU', 'area': 'HU'},
{'code': '10YIE-1001A00010',  'desc': 'MBA|SEM(EirGrid), SCA|IE, CTA|IE, Ireland (IE)'},
{'code': '10YIT-GRTN-----B',  'desc': 'Italy (IT), CTA|IT, SCA|IT, MBA|IT, LFB|IT, LFA|IT'},
{'code': '10YLT-1001A0008Q',  'desc': 'MBA|LT, SCA|LT, CTA|LT, Lithuania (LT), BZN|LT', 'area': 'LT'},
{'code': '10YLU-CEGEDEL-NQ',  'desc': 'Luxembourg (LU), CTA|LU'},
{'code': '10YLV-1001A00074',  'desc': 'CTA|LV, Latvia (LV), BZN|LV, SCA|LV, MBA|LV', 'area': 'LV'},
{'code': '10YMK-MEPSO----8',  'desc': 'MBA|MK, SCA|MK, BZN|MK, North Macedonia (MK), CTA|MK, LFA|MK', 'area': 'MK'},
{'code': '10YNL----------L',  'desc': 'LFA|NL, LFB|NL, CTA|NL, Netherlands (NL), BZN|NL, SCA|NL, MBA|NL', 'area': 'NL'},
{'code': '10YNO-0--------C',  'desc': 'MBA|NO, SCA|NO, Norway (NO), CTA|NO'},
{'code': '10YNO-1--------2',  'desc': 'BZN|NO1, IBA|NO1, IPA|NO1, SCA|NO1, MBA|NO1', 'area': 'NO1'},
{'code': '10YNO-2--------T',  'desc': 'MBA|NO2, SCA|NO2, IPA|NO2, IBA|NO2, BZN|NO2', 'area': 'NO2'},
{'code': '10YNO-3--------J',  'desc': 'BZN|NO3, IBA|NO3, IPA|NO3, SCA|NO3, MBA|NO3', 'area': 'NO3'},
{'code': '10YNO-4--------9',  'desc': 'MBA|NO4, SCA|NO4, IPA|NO4, IBA|NO4, BZN|NO4', 'area': 'NO4'},
{'code': '10YPL-AREA-----S',  'desc': 'BZN|PL, Poland (PL), CTA|PL, SCA|PL, MBA|PL, BZA|PL, LFA|PL', 'area': 'PL'},
{'code': '10YPT-REN------W',  'desc': 'LFA|PT, LFB|PT, MBA|PT, SCA|PT, CTA|PT, Portugal (PT), BZN|PT', 'area': 'PT'},
{'code': '10YRO-TEL------P',  'desc': 'BZN|RO, Romania (RO), CTA|RO, SCA|RO, MBA|RO, LFB|RO, LFA|RO', 'area': 'RO'},
{'code': '10YSE-1--------K',  'desc': 'MBA|SE, SCA|SE, CTA|SE, Sweden (SE)'},
{'code': '10YSI-ELES-----O',  'desc': 'Slovenia (SI), BZN|SI, CTA|SI, SCA|SI, MBA|SI, LFA|SI', 'area': 'SI'},
{'code': '10YSK-SEPS-----K',  'desc': 'LFA|SK, LFB|SK, MBA|SK, SCA|SK, CTA|SK, BZN|SK, Slovakia (SK)', 'area': 'SK'},
{'code': '10YTR-TEIAS----W',  'desc': 'Turkey (TR), BZN|TR, CTA|TR, SCA|TR, MBA|TR, LFB|TR, LFA|TR', 'area': 'TR'},
{'code': '10YUA-WEPS-----0',  'desc': 'LFA|UA-BEI, LFB|UA-BEI, MBA|UA-BEI, SCA|UA-BEI, CTA|UA-BEI, BZN|UA-BEI', 'area': 'UA-BEI'},
{'code': '11Y0-0000-0265-K',  'desc': 'BZN|GB(ElecLink)', 'area': 'GB(ElecLink)'},
{'code': '17Y0000009369493',  'desc': 'BZN|GB(IFA2)', 'area': 'GB(IFA2)'},
{'code': '46Y000000000007M',  'desc': 'BZN|DK1-NO1', 'area': 'DK1-NO1'},
{'code': '50Y0JVU59B4JWQCU',  'desc': 'BZN|NO2NSLBY Belarus (BY)', 'area': 'NO2NSLBY'},
{'code': 'RU',  'desc': 'Russia (RU)', 'area': 'RU'},
{'code': 'IS',  'desc': 'Iceland (IS)', 'area': 'IS'}
]