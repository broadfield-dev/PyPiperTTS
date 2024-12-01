import subprocess
import os
import json
import uuid
import requests

class PyPiper():
    def __init__(self):
        if not os.path.isdir(f'{os.getcwd()}/voices'):
            os.mkdir(f'{os.getcwd()}/voices')
        if not os.path.isfile(f'{os.getcwd()}/voices/voices.json'):
            voice_file=requests.get("https://huggingface.co/rhasspy/piper-voices/raw/main/voices.json")
            #print(voice_file.content)
            with open(f'{os.getcwd()}/voices/voices.json','wb') as w:
                w.write(voice_file.content)
            w.close()
            #subprocess.run(f"wget -O {os.getcwd()}/voices/voices.json https://huggingface.co/rhasspy/piper-voices/raw/main/voices.json", shell=True)
        with open(f"{os.getcwd()}/voices/voices.json","rb") as file:
            voice_main=json.loads(file.read())
        file.close()
        print(len(voice_main))
        self.key_list=list(voice_main.keys())
        self.model="en_US-joe-medium"

    def load_mod(self, instr="en_US-joe-medium"):
        self.model=instr
        lang=instr.split("_")[0]
        dia=instr.split("-")[0]
        name=instr.split("-")[1]
        style=instr.split("-")[2]
        file=f'{instr}.onnx'
        print(f"Loading model: {file}")
        if not os.path.isfile(f'{os.getcwd()}/voices/{file}'):
            print(f"Model not found locally")
            m_path= f"https://huggingface.co/rhasspy/piper-voices/resolve/main/{lang}/{dia}/{name}/{style}/{file}"
            print("Downloading json...")
            json_file=requests.get(f"{m_path}.json")
            print("Downloading model...")
            mod_file=requests.get(m_path)
            with open(f'{os.getcwd()}/voices/{file}','wb') as m:
                m.write(mod_file.content)
            m.close()
            with open(f'{os.getcwd()}/voices/{file}.json','wb') as j:
                j.write(json_file.content)
            j.close()
            #subprocess.run(f"wget -O {os.getcwd()}/voices/{file} {m_path}", shell=True)
            #subprocess.run(f"wget -O {os.getcwd()}/voices/{file}.json {m_path}.json", shell=True)
        with open(f'{os.getcwd()}/voices/{file}.json','rb') as f:
            self.json_ob=f.read()
        f.close
        print("Model Loaded")
        #return json_ob
    def tts(self, in_text,model,length=2,noise=0.1,width=1,sen_pause=1):
        text = in_text.replace(". ",".\n")
        model_path=f'{os.getcwd()}/voices/{model}.onnx'
        json_path=f'{os.getcwd()}/voices/{model}.onnx.json'
        output_file = f"{uuid.uuid4()}.wav"
        command = f"""echo '{text}' | piper --model {model_path} --config {json_path} --output_file {output_file} /
        --length_scale {length} --noise_scale {noise} --noise_w {width} --sentence_silence {sen_pause}"""
        subprocess.run(command, shell=True)
        return output_file
    def save_set(model,length,noise,width,sen_pause):
        if not os.path.isdir(f'{os.getcwd()}/saved'):
            os.mkdir(f'{os.getcwd()}/saved')
        set_json={"model":model,"length":length,"noise":noise,"width":width,"pause":sen_pause}
        file_name=f'{model}__{length}__{noise}__{width}__{sen_pause}'.replace(".","_")
        with open(f'{os.getcwd()}/saved/{file_name}.json','w') as file:
            file.write(json.dumps(set_json,indent=4))
        file.close()
        return(f'{file_name}.json')
    def load_set(set_file):
        with open(set_file,'r') as file:
            set_json=json.loads(file.read())
        file.close()
        return(set_json['model'],set_json['length'],
            set_json['noise'],set_json['width'],
            set_json['pause'])
    def exp(exp_file):
        txt="""PiperTTS is a powerful text-to-speech TTS node designed to convert written text into high-quality spoken audio. This node leverages advanced voice synthesis models to generate natural-sounding speech, making it an invaluable tool for AI developers looking to add a vocal element to their projects."""
        exp_file=f"./example/en_US-ljspeech-high_2__21_0__88_0__22_2__6.json"
        return(txt,exp_file)
