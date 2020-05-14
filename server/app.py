from flask import Flask, request, redirect
from flask_restful import Api, Resource, reqparse
from csv import writer
import os
import pandas
import textract

app = Flask(__name__)
api = Api(app)

filepath = 'C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\models.csv'

cvs = [
    {
        "name": "",
        "text": "",
        "tags": "",
        "fileExtension": "",
        "fileContent": "",
    }
]

class Uploads(Resource):
    def get(self, name):

        parser = reqparse.RequestParser()
        parser.add_argument("model_id")
        args = parser.parse_args()

        path = "C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\models\\" + name + "\\" + args["model_id"]

        tags_path = "C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\models\\" + name + "\\" + args["model_id"] + "\\tags.csv"
        print(tags_path)
        df2 = pandas.read_csv(tags_path)
        
        files = []
        # r = root, d = directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.pdf' in file:

                    # Get pdfs uploaded by user                 
                    text = textract.process(path + "\\" + file, encoding='utf-8')
                    dtext = text.decode("utf-8") 
                    stext= dtext.split()
                    
                    # Get already tagged text from uploaded files
                    tags = ""
                    #for i in df.index:
                    #    if df['filename'][i] == file:
                    #       tags = df['tags'][i]
                    #        #break

                    single_file = {
                        "name": file,
                        "text": stext,
                        "tags": tags,
                        "fileExtension": "",
                        "fileContent": ""          
                    }
                    files.append(single_file)

        return files

    def post(self, name):

        parser = reqparse.RequestParser()
        parser.add_argument("filename")
        parser.add_argument("tags")
        parser.add_argument("model_id")
        args = parser.parse_args()

        if args["tags"] is not None:
            path = "C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\models\\" + name + "\\" + args["model_id"] + "\\tags.csv"
            if not os.path.exists(path):
                f = open(path, "wb")  
                f.close()

                row_contents = ["filename", "tags"]
                row_contents2 = [args["filename"], args["tags"]]
        
                with open(path, 'w', newline='') as write_obj:
                    csv_writer = writer(write_obj)
                    csv_writer.writerow(row_contents)
                    csv_writer.writerow(row_contents2)
            else:
                row_contents = [args["filename"], args["tags"]]
        
                with open(path, 'a+', newline='') as write_obj:
                    csv_writer = writer(write_obj)
                    csv_writer.writerow(row_contents)

        else:
            filename = request.headers.get('Slug')
            model_id = request.headers.get('Content-Type')

            path = "C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\models\\" + name + "\\" + model_id

            if not os.path.exists(path):
                os.makedirs(path)
            
            path = path + "\\" + filename

            if not os.path.exists(path):
                f = open(path, "wb")
                f.write(request.data)
                f.close()

class Models(Resource):
    def get(self, name):
        
        parser = reqparse.RequestParser()
        parser.add_argument("model_id")
        args = parser.parse_args()
        
        models = []
        print(filepath)
        df = pandas.read_csv(filepath)
             
        if args["model_id"] is not None:
            # Retornar o último registo criado (com o id mais elevado)
            if args["model_id"] == 0:            
                model_id = 0
                for i in df.index:
                    if df['userId'][i] == name and df['model_id'][i] > model_id:
                        model = {   "user_id": df['userId'][i],
                                    "model_id": str(df['model_id'][i]),
                                    "model_name": df['model_name'][i],
                                    "model_status": df['status'][i] }
                
                return model       
            # Retornar um registo específico de acordo com o id
            else:
                for i in df.index:
                    if df['userId'][i] == name and str(df['model_id'][i]) == args["model_id"]:
                        model = {   "user_id": df['userId'][i],
                                    "model_id": str(df['model_id'][i]),
                                    "model_name": df['model_name'][i],
                                    "model_status": df['status'][i] }
                
                        return model

        # Retornar todos os registos para o user em questão
        else:            
            for i in df.index:         
                model = { 
                    "user_id": df['userId'][i],
                    "model_id": str(df['model_id'][i]),
                    "model_name": df['model_name'][i],
                    "model_status": df['status'][i]
                }
                models.append(model)

            return models
    
    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("model_name")
        args = parser.parse_args()
        
        models = []
        df = pandas.read_csv(filepath)

        model = 0
        for i in df.index:
            if df['userId'][i] == name and int(df['model_id'][i]) > model:
                model = int(df['model_id'][i])
        model = model + 1
        row_contents = [name, model, args["model_name"],'created']
        
        with open(filepath, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(row_contents)

class User(Resource):
    def get(self, name):
        for user in cvs:
            if(name == user["name"]):
                return user, 200             
        return "User not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("tags")
        parser.add_argument("fileExtension")
        parser.add_argument("fileContent")

        args = parser.parse_args()
        print(args["tags"])

        for user in cvs:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400

        stext = 'teste'
        # nao funciona csv rtf txt jpeg
        if args['fileExtension'] == 'doc': #or args['fileExtension'] == 'docx':
            import base64
            import io
            decoded = base64.b64decode(args['fileContent'])
            fp = io.BytesIO(decoded)

            f = open("C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\cvs\\basetest" + name + ".doc", "wb")
            f.write(fp.getbuffer())
            f.close()

            import textract
            text = textract.process("C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\cvs\\basetest" + name + ".doc", encoding='utf-8')
            dtext = text.decode("utf-8") 
            stext= dtext.split()

            #text.rstrip('\r\n')
            print(stext)


            #import docx
            #doc = docx.Document("C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\basetest.doc")
            #fullText = []
            #for para in doc.paragraphs:
            #    fullText.append(para.text)
            #varfulltext = '\n'.join(fullText)


            #teste = "Exposição é um tipo de discurso cuja principal finalidade é transmitir informação. É uma das formas de expressão próprias dos textos didáticos. A finalidade de transmitir informação pode concretizar-se de modos muito distintos, seja na língua oral, seja na escrita."
            #x = teste.split()

        if args['fileExtension'] == 'docx': #or args['fileExtension'] == 'docx':
            import base64
            import io
            decoded = base64.b64decode(args['fileContent'])
            fp = io.BytesIO(decoded)

            f = open("C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\cvs\\basetest" + name + ".docx", "wb")
            f.write(fp.getbuffer())
            f.close()

            import textract
            text = textract.process("C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\cvs\\basetest" + name + ".docx", encoding='utf-8')
            dtext = text.decode("utf-8") 
            stext= dtext.split()

            print(stext)

        if args['fileExtension'] == 'pdf': #or args['fileExtension'] == 'docx':
            import base64
            import io
            decoded = base64.b64decode(args['fileContent'])
            fp = io.BytesIO(decoded)

            f = open("C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\cvs\\basetest" + name + ".pdf", "wb")
            f.write(fp.getbuffer())
            f.close()

            import textract
            text = textract.process("C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\cvs\\basetest" + name + ".pdf", encoding='utf-8')
            dtext = text.decode("utf-8") 
            stext= dtext.split()

            print(stext)

            if stext == '':
                from PIL import Image 
                import pytesseract 
                import sys 
                from pdf2image import convert_from_path 
                import os 
                pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                
                PDF_file = "C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\cvs\\basetest" + name + ".pdf"
                pages = convert_from_path(PDF_file, 500) 
                image_counter = 1
                
                for page in pages: 
                
                    filename = "page_"+str(image_counter)+".jpg"
                    page.save(filename, 'JPEG')
                    image_counter = image_counter + 1

                filelimit = image_counter-1
                outfile = "out_text.txt"
                f = open(outfile, "a") 
                
                for i in range(1, filelimit + 1): 
                
                    filename = "page_"+str(i)+".jpg"
                    text = str(((pytesseract.image_to_string(Image.open(filename))))) 
                    text = text.replace('-\n', '')     
                
                    f.write(text) 
                 
                f.close()
                text = textract.process("C:\\Users\\LABS\\Documents\\Python Scripts\\pdftotext\\out_text.txt", encoding='utf-8')
                dtext = text.decode("utf-8") 
                stext= dtext.split()


            

        user = {
            "name": name,
            "text": stext,
            "tags": args["tags"],
            "fileExtension": args["fileExtension"],
            "fileContent": args["fileContent"]          
        }
        cvs.append(user)

        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("occupation")
        parser.add_argument("tags")
        args = parser.parse_args()

        for user in cvs:
            if(name == user["name"]):
                user["text"] = args["text"]
                user["occupation"] = args["occupation"]
                user["tags"] = args["tags"]
                return user, 200
        
        user = {
            "name": name,
            "text": args["text"],
            "occupation": args["occupation"],
            "tags": args["tags"]
        }
        cvs.append(user)
        return user, 201

    def delete(self, name):
        global cvs
        cvs = [user for user in cvs if user["name"] != name]
        return "{} is deleted.".format(name), 200

api.add_resource(User, "/user/<string:name>")
api.add_resource(Models, "/models/<string:name>")
api.add_resource(Uploads, "/uploads/<string:name>")

app.run(debug=True)