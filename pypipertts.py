import subprocess
import os
import io
import json
import uuid
import requests
from pydub import AudioSegment
from pydub.silence import split_on_silence

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
        self.json_ob=f'{os.getcwd()}/voices/{file}.json'
        print("Model Loaded")
    
    def tts(self, in_text,model="",length=2,noise=0.1,width=1,sen_pause=1):
        if not model:
            model=self.model
        self.load_mod(instr=model)
        text = in_text.replace(". ",".\n")
        model_path=f'{os.getcwd()}/voices/{model}.onnx'
        json_path=f'{os.getcwd()}/voices/{model}.onnx.json'
        output_file = f"{uuid.uuid4()}.wav"
        command = f"""echo '{text}' | piper --model {model_path} --config {json_path} --output_file {output_file}\
        --length_scale {length} --noise_scale {noise} --noise_w {width} --sentence_silence {sen_pause}"""
        subprocess.run(command, shell=True)
        return output_file

    def stream_tts(self, in_text,model="",length=1,noise=1,width=1,sen_pause=1):
        if not model:
            model=self.model
        text=in_text
        #text = in_text.replace(". ",".\n")
        model_path=f'{os.getcwd()}/voices/{model}.onnx'
        json_path=f'{os.getcwd()}/voices/{model}.onnx.json'
        command = f"""echo '{text}' | piper --model {model_path} --config {json_path} --output-raw\
        --length_scale {length} --noise_scale {noise} --noise_w {width} --sentence_silence {sen_pause}"""
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        buffer = io.BytesIO()
        while True:
            data = process.stdout.read(88200)
            if not data:
                    break
            audio_segment = AudioSegment(
                data=data,
                sample_width=2,
                frame_rate=22050,
                channels=1
            )
            audio_chunks = split_on_silence(
                audio_segment, 
                min_silence_len=5000,
                silence_thresh=-16,
                keep_silence=100
            )
            for chunk in audio_chunks:
                chunk.export(buffer, format="wav")
                self.buffer=buffer.getvalue()
                yield buffer.getvalue()
    
    def save_set(self,model,length,noise,width,sen_pause):
        if not os.path.isdir(f'{os.getcwd()}/saved'):
            os.mkdir(f'{os.getcwd()}/saved')
        set_json={"model":model,"length":length,"noise":noise,"width":width,"pause":sen_pause}
        file_name=f'{model}__{length}__{noise}__{width}__{sen_pause}'.replace(".","_")
        with open(f'{os.getcwd()}/saved/{file_name}.json','w') as file:
            file.write(json.dumps(set_json,indent=4))
        file.close()
        return(f'{file_name}.json')
        
    def load_set(self,set_file):
        with open(set_file,'r') as file:
            set_json=json.loads(file.read())
        file.close()
        return(set_json['model'],set_json['length'],
            set_json['noise'],set_json['width'],
            set_json['pause'])
