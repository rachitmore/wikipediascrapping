import logging
from flask import Flask,request,render_template
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json

logging.basicConfig(filename="application.log",
                    format='%(asctime)s %(message)s', filemode='w', level=logging.DEBUG)

app =Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST']) # To render Homepage
@cross_origin()
def home_page():
    return render_template('index.html')

@app.route('/info', methods=['POST'])
@cross_origin()
def infomation():
    try:
        if (request.method=='POST'):
            logging.info("Page is Searched")

            search_string = request.form['content']
            logging.info(f"Value received from user-{search_string}")
            

            search_string = search_string.replace(" ","_")
            wiki_link = "https://en.wikipedia.org/wiki/"

            wiki = wiki_link + search_string
            logging.info(f"wikipedia_links is - {wiki}")

            try:
                uclient = uReq(wiki)
                logging.info("URL responded")
            except Exception as e:
                logging.info(e)

            wiki_page = uclient.read()
            uclient.close()

            try:
                soup = bs(wiki_page,"html.parser")
                logging.info("Soup has been created")
            except Exception as e:
                logging.info(e)

            title = soup.title.string
            title = title.replace("Wikipedia","")
            title = title.replace("-","")
            title = title.strip()
            logging.info(f"Got the title - {title}")

            try:
                soup_list =  soup.get_text().replace("\n","  ").split("  ")
                logging.info("Soup List has been created")
            except Exception as e:
                logging.info(e)

            try:
                for j in range(3):
                    for i in soup_list:
                        if len(i)<500:
                            soup_list.remove(i)
            except Exception as e:
                logging.info(e)


            language = "العربيةঅসমীয়াAzərbaycancaবাংলাBân-lâm-gúБеларускаяभोजपुरीБългарскиབོད་ཡིགBosanskiCatalàČeštinaCymraegDanskالدارجةDeutschEestiΕλληνικάEspañolEuskaraفارسیFrançaisGalego한국어Հայերենहिन्दीBahasa IndonesiaIsiZuluÍslenskaItalianoעבריתಕನ್ನಡLatviešuLietuviųMagyarМакедонскиമലയാളംमराठीBahasa MelayuМонголNederlands日本語Norsk bokmålNorsk nynorskOccitanଓଡ଼ିଆپنجابیPolskiPortuguêsRomânăRuna SimiРусскийᱥᱟᱱᱛᱟᱲᱤShqipSimple EnglishSlovenščinaکوردیСрпски / srpskiSrpskohrvatski / српскохрватскиSuomiSvenskaTagalogతెలుగుไทยTürkçeУкраїнськаاردوئۇيغۇرچە / UyghurcheTiếng ViệtVõro吴语粵語中文"
            extra = "Main pageContentsCurrent eventsRandom articleAbout WikipediaContact usDonate HelpLearn to editCommunity portalRecent changesUpload file Language links are at the top of the page across from the title. What links hereRelated changesUpload fileSpecial pagesPermanent linkPage informationCite this pageWikidata item"
            extra1 = 'Publishing  Retrieved from "https://en.wikipedia.org/w/index.php?title=Data_science&oldid=1148229141" Categories: Information scienceComputer occupationsComputational fields of studyData analysisHidden categories: Articles with short descriptionShort description is different from WikidataUse dmy dates from August 2021  This page was last edited on 4 April 2023, at 21:32\xa0(UTC). Text is available under the Creative Commons Attribution-ShareAlike License 3.0; By using this site, you agree to the Terms of Use and Privacy Policy. Wikipedia® is a registered trademark of the Wikimedia Foundation, Inc., a non-profit organization.'

            soup_string = " "
            soup_string = soup_string.join(soup_list)
            soup_string = soup_string.replace(extra,"").strip()
            soup_string = soup_string.replace(extra1,"").strip()

            for i in range(100):
                soup_string = soup_string.replace(f"[{i}]",',')
                soup_string = soup_string.replace(".,",'.')

            wikipedia = [title,soup_string,language]
            
            logging.info("result generated")

            return render_template("result.html",wikipedia = wikipedia)
        else:
            print("Something went wrong")
        
    except Exception as e:
        logging.info(e)
        return e

if __name__ == "__main__":
   app.run(debug=True)
   app.run(host='0.0.0.0', port=5000)
