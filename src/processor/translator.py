import time
import torch
from transformers import AutoModelForSeq2SeqLM
from IndicTransTokenizer import IndicProcessor, IndicTransTokenizer

class Translator:
    """Translates sentences from one language to another using the IndicTrans model."""
    def __init__(self, model_name="ai4bharat/indictrans2-indic-en-dist-200M", direction="indic-en"):
        """Initializes the translator with the model and tokenizer."""
        self.tokenizer = IndicTransTokenizer(direction)
        self.ip = IndicProcessor(inference=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)

    def translate_sentences(self, src_lang, tgt_lang, sentences):
        """Translates a list of sentences from the source language to the target language."""
        batch = self.ip.preprocess_batch(sentences, src_lang, tgt_lang)
        batch = self.tokenizer(batch, src=True, return_tensors="pt")
        with torch.inference_mode():
            outputs = self.model.generate(**batch, num_beams=5, num_return_sequences=1, max_length=256)
        outputs = self.tokenizer.batch_decode(outputs, src=False)
        outputs = self.ip.postprocess_batch(outputs, lang="eng_Latn")
        return outputs

if __name__ == "__main__":
    # inference te to en
    translator = Translator()
    sentences = [
        "శ్రీకైవల్యపదంబు.",
        "శ్రీ",
        "తెలుగుల పుణ్యపేటి బమ్మెర పోతన శ్రీమద్భాగవత అమృతాన్ని తెలుగుజాతికి అందించటానికి పూనుకొని ముందుగా నందాంగనా డింభకుడైన శ్రీకృష్ణపరమాత్మను హృదయంలో నిలుపుకుంటున్నాడు",
    ]
    print("TE to EN")
    start_time = time.time()
    translations = translator.translate_sentences("tel_Telu", "eng_Latn", sentences)
    end_time = time.time()
    print(f"Time taken to translate poems: {end_time - start_time} seconds")
    print(translations)

    # inference te to hi
    print("TE to HI")
    translator = Translator(model_name="ai4bharat/indictrans2-indic-indic-dist-320M", direction="indic-indic")
    translations = translator.translate_sentences("tel_Telu", "hin_Deva", sentences)
    print(translations)
