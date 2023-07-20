import os
import re
from googletrans import Translator
from time import sleep
import json
import random

# TODO
# gtfo with the line breaks, engine word wraps dynamically anyway
# apply possible translations
# apply string difference checker

dictionary = {}
with open("dictionary.json", "r") as o:
    dictionary = json.load(o)
with open("custom_dictionary.json", "r") as o:
    d = json.load(o)
    for i in d:
        dictionary[i] = d[i]
translator = Translator()

languages = [
    "ar", # Arabic
    "zh-CN", # Chinese (Simplified)
    "da", # Danish
    #"nl", # Dutch
    "eo", # Esperanto
    "fi", # Finnish
    "fr", # French
    "de", # German
    "el", # Greek
    "hi", # Hindi
    "id", # Indonesian
    "it", # Italian
    "ja", # Japanese
    "ko", # Korean
    "pl", # Polish
    "pt", # Portuguese
    "ru", # Russian
    "es", # Spanish
    #"sv", # Swedish
    "th", # Thai
    "cy", # Welsh
    "en"  # English
]
passes = 25

replacements = [
    ("<Cap><DEF_ART_ACTOR>",               "[◍]", "[\[\(]\s*◍\s*[\]\)]", "<Cap><DEF_ART_ACTOR>"),
    ("<Cap><DEF_ART_TARGET>",              "[◎]", "[\[\(]\s*◎\s*[\]\)]", "<Cap><DEF_ART_TARGET>"),
    ("<Cap><INDEF_ART_SGL_I_NAME_0>",      "[♠]", "[\[\(]\s*♠\s*[\]\)]", "<Cap><INDEF_ART_SGL_I_NAME_0>"),
    ("<Cap><TEAM_NAME>",                   "[♡]", "[\[\(]\s*♡\s*[\]\)]", "<Cap><TEAM_NAME>"),
    ("<Cap><character_0>",                 "[♢]", "[\[\(]\s*♢\s*[\]\)]", "<Cap><character_0>"),
    ("<Cap><character_1>",                 "[♣]", "[\[\(]\s*♣\s*[\]\)]", "<Cap><character_1>"),
    ("<Cap><character_2>",                 "[♤]", "[\[\(]\s*♤\s*[\]\)]", "<Cap><character_2>"),
    ("<Cap><hero>",                        "[♥]", "[\[\(]\s*♥\s*[\]\)]", "<Cap><hero>"),
    ("<Cap><leader>",                      "[♚]", "[\[\(]\s*♚\s*[\]\)]", "<Cap><leader>"),
    ("<Cap><most_heroic>",                 "[♧]", "[\[\(]\s*♧\s*[\]\)]", "<Cap><most_heroic>"),
    ("<Cap><nickname>",                    "[♛]", "[\[\(]\s*♛\s*[\]\)]", "<Cap><nickname>"),
    ("<Cap><string_0>",                    "[♜]", "[\[\(]\s*♜\s*[\]\)]", "<Cap><string_0>"),
    ("<Cap><string_1>",                    "[♝]", "[\[\(]\s*♝\s*[\]\)]", "<Cap><string_1>"),
    ("<Cap><string_2>",                    "[♞]", "[\[\(]\s*♞\s*[\]\)]", "<Cap><string_2>"),
    ("<Cap><string_3>",                    "[☋]", "[\[\(]\s*☋\s*[\]\)]", "<Cap><string_3>"),
    ("<Cap><string_4>",                    "[☊]", "[\[\(]\s*☊\s*[\]\)]", "<Cap><string_4>"),
    ("<Cap>",                              "[☀]", "[\[\(]\s*☀\s*[\]\)]", "<Cap>"),
    ("<ACTION_0>",                         "[☁]", "[\[\(]\s*☁\s*[\]\)]", "<ACTION_0>"),
    ("<DEF_ART_ACTOR>",                    "[☂]", "[\[\(]\s*☂\s*[\]\)]", "<DEF_ART_ACTOR>"),
    ("<DEF_ART_TARGET>",                   "[☃]", "[\[\(]\s*☃\s*[\]\)]", "<DEF_ART_TARGET>"),
    ("<DEF_ART_ACTION>",                   "[☄]", "[\[\(]\s*☄\s*[\]\)]", "<DEF_ART_ACTION>"),
    ("<INDEF_ART_ACTION>",                 "[℄]", "[\[\(]\s*℄\s*[\]\)]", "<INDEF_ART_ACTION>"),
    ("<INDEF_ART_SGL_I_NAME_0>",           "[↪]", "[\[\(]\s*↪\s*[\]\)]", "<INDEF_ART_SGL_I_NAME_0>"),
    ("<INDEF_ART_SGL_I_NAME_1>",           "[⇶]", "[\[\(]\s*⇶\s*[\]\)]", "<INDEF_ART_SGL_I_NAME_1>"),
    ("<INDEF_ART_SGL_I_NAME_2>",           "[⇱]", "[\[\(]\s*⇱\s*[\]\)]", "<INDEF_ART_SGL_I_NAME_2>"),
    ("<PLR_I_NAME_0>",                     "[⋘]", "[\[\(]\s*⋘\s*[\]\)]", "<PLR_I_NAME_0>"),
    ("<SGL_I_NAME_0>",                     "[∰]", "[\[\(]\s*∰\s*[\]\)]", "<SGL_I_NAME_0>"),
    ("<SGL_I_NAME_1>",                     "[⋙]", "[\[\(]\s*⋙\s*[\]\)]", "<SGL_I_NAME_1>"),
    ("<SGL_I_NAME_2>",                     "[⊠]", "[\[\(]\s*⊠\s*[\]\)]", "<SGL_I_NAME_2>"),
    ("<TEAM_NAME>",                        "[⊡]", "[\[\(]\s*⊡\s*[\]\)]", "<TEAM_NAME>"),
    ("<character_0>",                      "[⊕]", "[\[\(]\s*⊕\s*[\]\)]", "<character_0>"),
    ("<character_1>",                      "[⊖]", "[\[\(]\s*⊖\s*[\]\)]", "<character_1>"),
    ("<character_2>",                      "[⊗]", "[\[\(]\s*⊗\s*[\]\)]", "<character_2>"),
    ("<hero>",                             "[⊘]", "[\[\(]\s*⊘\s*[\]\)]", "<hero>"),
    ("<leader>",                           "[⊙]", "[\[\(]\s*⊙\s*[\]\)]", "<leader>"),
    ("<most_heroic>",                      "[⊚]", "[\[\(]\s*⊚\s*[\]\)]", "<most_heroic>"),
    ("<nickname>",                         "[⊛]", "[\[\(]\s*⊛\s*[\]\)]", "<nickname>"),
    ("<string_0>",                         "[⊜]", "[\[\(]\s*⊜\s*[\]\)]", "<string_0>"),
    ("<string_1>",                         "[⊝]", "[\[\(]\s*⊝\s*[\]\)]", "<string_1>"),
    ("<string_2>",                         "[⊞]", "[\[\(]\s*⊞\s*[\]\)]", "<string_2>"),
    ("<string_3>",                         "[⊟]", "[\[\(]\s*⊟\s*[\]\)]", "<string_3>"),
    ("<string_4>",                         "[⊰]", "[\[\(]\s*⊰\s*[\]\)]", "<string_4>"),
    ("<val_0>",                            "[⊱]", "[\[\(]\s*⊱\s*[\]\)]", "<val_0>"),
    ("<val_1>",                            "[▀]", "[\[\(]\s*▀\s*[\]\)]", "<val_1>"),
    ("<val_2>",                            "[▩]", "[\[\(]\s*▩\s*[\]\)]", "<val_2>"),
    ("<val_3>",                            "[▨]", "[\[\(]\s*▨\s*[\]\)]", "<val_3>"),
    ("<val_4>",                            "[▧]", "[\[\(]\s*▧\s*[\]\)]", "<val_4>"),
    ("<val_5>",                            "[▦]", "[\[\(]\s*▦\s*[\]\)]", "<val_5>"),
    ("<val_6>",                            "[▥]", "[\[\(]\s*▥\s*[\]\)]", "<val_6>"),
    ("<val_7>",                            "[▤]", "[\[\(]\s*▤\s*[\]\)]", "<val_7>"),
    ("<val_8>",                            "[▣]", "[\[\(]\s*▣\s*[\]\)]", "<val_8>"),
]

#paths = ["romfs\\data\\Script\\field\\message\\eng\\npc\\m01.binE", "romfs\\data\\Script\\field\\message\\eng\\npc\\m01b.binE",
#    "romfs\\data\\Message\\eng\\msg_action.binE", "romfs\\data\\Message\\eng\\msg_church.binE", "romfs\\data\\Message\\eng\\msg_common.binE",
#    "romfs\\data\\Message\\eng\\msg_item.binE", "romfs\\data\\Message\\eng\\msg_equipment.binE", "romfs\\data\\Message\\eng\\msg_menu.binE",
#    "romfs\\data\\Message\\eng\\msg_monster.binE"]
paths = ["romfs\\data\\Message", "romfs\\data\\Script", "romfs\\data\\Params"]
skip_files = []
#escapes = []

def start():
    json_files = []

    for i in paths:
        json_files += search_subfolders(i)

    for file in json_files:
        if file in skip_files:
            continue
        if not file.endswith(".json"):
            continue

        j = ""
        with open(file, "r") as o:
            j = json.load(o)

        #if len(j["strings"]) <= 1:
        #    print(file)
        #continue

        name = re.search("[^\\\\/]*?$", file).group()
        path = re.search(".*[\\\\/]", file).group()

        if not os.path.exists(f"out/{path}"):
            os.makedirs(f"out/{path}")

        print(file)
        if file.endswith(".binE.json"):
            out = translate_binE(j)
        elif file.endswith(".txt.json"):
            out = translate_txt(j)
        else:
            continue
        #continue

        if file.endswith(".binE.json"):
            with open(f"out/{path}{name}", "w") as o:
                json.dump(out, o)
        elif file.endswith(".txt.json"):
            with open(f"out/{path}{name[:-5]}", "w") as o:
                o.write("\r".join(out))
        #with open("dictionary.json", "w") as o:
        #    json.dump(dictionary, o)

class BinE:
    def __init__(self, bin: bytes):
        if len(bin) < 16:
            self.strings = []
            self.pointers = []
            self.header = bin
            return

        last_end_index = -1
        penultimate_end_index = -1
        for i in range(5, len(bin)):
            chunk = bytes()
            if i == 5:
                chunk = bin[-i:]
            else:
                chunk = bin[-i:-i+5]
            
            if chunk.decode(errors="ignore") == "[end]" and last_end_index == -1:
                last_end_index = len(bin) - i
                continue

            if chunk.decode(errors="ignore") == "[end]" and penultimate_end_index == -1:
                penultimate_end_index = len(bin) - i
                break

        last_message_index = penultimate_end_index + 5

        first_end_index = -1
        for i in range(len(bin)):
            if bin[i:i+5].decode(errors="ignore") == "[end]":
                first_end_index = i
                break
        
        last_pointer_index = -1
        i = first_end_index
        i = i - (i % 4)
        while i >= 0:
            if int.from_bytes(bin[i:i+4], "little") == last_message_index:
                last_pointer_index = i
                break
            else:
                i -= 4
        
        first_message_index = last_pointer_index + 4

        first_pointer_index = -1
        i = last_pointer_index
        while i >= 0:
            if int.from_bytes(bin[i:i+4], "little") == first_message_index:
                first_pointer_index = i
                break
            i -= 4

        self.header = bin[0:first_pointer_index]

        self.pointers = []
        for i in range(first_pointer_index, int.from_bytes(bin[first_pointer_index:first_pointer_index+4], "little"), 4):
            self.pointers.append(int.from_bytes(bin[i:i+4], "little"))

        self.strings = []
        for ptr in self.pointers:
            self.strings.append(re.search("[\S\s]*?(?=\[end\])", bin[ptr:].decode(errors="ignore")).group())
        
        self.raw = bin
    
    def update(self):
        end_strings = []
        for string in self.strings:
            end_strings.append(f"{string}[end]")
        
        string_count = len(end_strings)

        first_pointer_index = len(self.header)
        first_string_index = first_pointer_index + (string_count * 4)

        pi = first_string_index
        for i in range(len(end_strings)):
            self.pointers[i] = pi
            pi += len(bytes(end_strings[i], encoding="utf-8"))
        
        self.raw = bytes(self.header)
        for ptr in self.pointers:
            self.raw += int.to_bytes(ptr, 4, "little")
        for string in end_strings:
            self.raw += bytes(string, encoding="utf-8")

def search_subfolders(path: str):
    if os.path.isfile(path):
        return [path]

    files = []

    sd = os.scandir(path)
    for i in sd:
        if i.is_file():
            files.append(i.path)
        if i.is_dir():
            files += search_subfolders(i.path)
    
    return files

def translate_binE(js: dict):

    for string_index in range(len(js["strings"])):
        if not js["strings"][string_index][1]:
            js["strings"][string_index] = js["strings"][string_index][0]
            continue

        string: str = js["strings"][string_index][0]

        #for i in re.findall("<[^<>]*?>", string):
        #    if i == "<x>":
        #        print("stop")
        #    if not i in escapes:
        #        escapes.append(i)
        #continue

        print(f"\u007B{string_index}: \"{string}\"\u007D")

        trans = translate_entry(string)

        js["strings"][string_index] = trans
    #return

    return js

def translate_txt(js: dict):

    for i in range(len(js)):
        if len(js[i]) < 1:
            js[i] = ""
            continue
        if not js[i][0]:
            js[i] = js[i][1]
            continue
        
        print(f"\u007B{i}: \"{js[i][1:-1]}\"\u007D")

        if len(js[i]) > 2:
            parse_list = js[i][1:-1]
        else:
            parse_list = js[i][1:]
        out_list = []
        for j in range(len(parse_list)):
            out_list.append(translate_entry(parse_list[0]))
        parse_list = out_list

        if len(js[i]) > 2:
            js[i] = "\t".join(parse_list) + "\t" + js[i][-1]
        else:
            js[i] = "\t".join(parse_list)

    return js

def translate_entry(string: str, bypass_charname: bool = False, dont_dic: bool = False) -> str:
    if len(string) <= 1 \
        or string.startswith("PARAMETER CHANGE") or string.startswith("MESSAGE ATTACK") or string.startswith("DO NOTHING") \
        or string.startswith("CALL SAME TYPE MONSTER") or string.startswith("CALL DIFF. TYPE MONSTER") \
        or string.startswith("DESCRIPTION OF ") \
        or string == "<empty>" or string == "EN_MISSING" \
        or re.search("^(<[^>]*?>|\W)*$", string): # <-- regex matches strings that contain only <escape codes> and non-words
        return string
    
    if string.lower() in dictionary:
        print(f"{string} -> {dictionary[string.lower()]}")
        return dictionary[string.lower()]
    
    if "<page>" in string:
        pages = re.split("<page>", string)
        trans_pages = []

        for page in pages:
            trans_pages.append(translate_entry(page))
        
        return "<page>".join(pages)
    
    prefix = re.search("^(<[^<>]*?voice_?[0-9A-Fx]*>|<se_[^>]*>|\*<?\:>? )*", string).group()
    if len(prefix) > 0:
        return prefix + translate_entry(string[len(prefix):])
    
    # parse IF_ statements here
    match = re.search(r"(<IF_([^<>]*?)>)(.*?)(<ELSE_NOT_\2>)(.*?)(<ENDIF_\2>)", string)
    if not match:
        match = re.search(r"(<IF_(ACT=TARGET)>)(.*?)(<ELSE_ACT!=TARGET>)(.*?)(<ENDIF_ACT=TARGET>)", string)
    if not match:
        match = re.search(r"(<IF_([^<>]*?)_SOLO>)(.*?)(<ELSE_\2_NOT_SOLO>)(.*?)(<ENDIF_\2_SOLO>)", string)
    if not match:
        match = re.search(r"(<IF_SING val_(\d)>)(.*?)(<ELSE_NOT_SING>)(.*?)(<ENDIF_SING>)", string)
    if (match):
        if_condition = match.group(1)
        else_condition = match.group(4)
        endif = match.group(6)

        match_if = match.group(3)
        match_else = match.group(5)

        pre = string[:match.start()]
        post = string[match.end():]

        print(f"{if_condition}{pre}{match_if}{post}{else_condition}{pre}{match_else}{post}{endif}")
        print("")

        return if_condition +\
            translate_entry(pre + match_if + post) +\
            else_condition +\
            translate_entry(pre + match_else + post) +\
            endif
    match = re.search(r"(<IF_(\w*?)_M>)(.*?)(<IF_\2_F>)(.*?)(<IF_\2_N>)(.*?)(<ENDIF_\2_MFN>)", string)
    if (match):
        m_condition = match.group(1)
        f_condition = match.group(4)
        n_condition = match.group(6)
        endif = match.group(8)

        match_m = match.group(3)
        match_f = match.group(5)
        match_n = match.group(7)

        pre = string[:match.start()]
        post = string[match.end():]

        print(f"{m_condition}{pre}{match_m}{post}{f_condition}{pre}{match_f}{post}{n_condition}{pre}{match_n}{post}{endif}")
        print()

        return m_condition +\
            translate_entry(pre + match_m + post) +\
            f_condition +\
            translate_entry(pre + match_f + post) +\
            n_condition +\
            translate_entry(pre + match_n + post) +\
            endif

    if ((not bypass_charname) and re.search("(?<!<)\:", string[:34])):
        charname, dialogue = re.split("(?<!<)\:\s*", string, maxsplit=1)
        
        return prefix + translate_entry(charname, True)[:33] + ": " + translate_entry(dialogue, True)
    
    # parse center statements here TODO

    in_string = string
    in_string = re.sub("<->", "-", in_string)
    in_string = re.sub("\[-\]", "", in_string)
    in_string = re.sub("<\.\.\.>", "...", in_string)
    in_string = re.sub("<\:>", ":", in_string)
    in_string = re.sub("<endash>", "\u2013", in_string)
    in_string = re.sub("<equal>", "=", in_string)
    in_string = re.sub("<x>", "\u00D7", in_string) #this won't be used but eh
    in_string = re.sub("\\\\n|\n", " ", in_string)
    #in_string = re.sub("\\\\", "", in_string)
    in_string = re.sub("<center>", "", in_string)

    for r in replacements:
        in_string = in_string.replace(r[0], r[1])

    translation = bad_translate(in_string)

    out_string = translation
    out_string = re.sub("【", "[", out_string) # do these before
    out_string = re.sub("】", "]", out_string) # parsing escapes

    for r in replacements:
        out_string = re.sub(r[2], r[3], out_string)

    out_string = re.sub("\\\\N", "\\\\n", out_string)
    out_string = re.sub("…", "...", out_string)
    out_string = re.sub("\uFF1F", "?", out_string)
    out_string = re.sub("\uFF01", "!", out_string)
    out_string = re.sub("\uFF5E", "~`", out_string)
    out_string = re.sub("\u200b", "", out_string)
    out_string = re.sub("\:", "<:>", out_string)
    out_string = re.sub("\u2013", "<endash>", out_string)
    out_string = re.sub("=", "<equal>", out_string)
    out_string = re.sub("\u00D7", "<x>", out_string)
    out_string = re.sub("<Cap>\s+", "<Cap>", out_string)

    dictionary[string.lower()] = out_string
    if (not dont_dic):
        with open("dictionary.json", "w") as o:
            json.dump(dictionary, o)
    print(f"{string} -> {out_string}")
    return out_string

def bad_translate(string):
    retry_count = 0
    while True:
        try:
            translated = string
            langs = ["en"]
            i = 0
            while i < passes:
                choice = random.choice(languages)
                if choice == langs[-1]:
                    continue
                else:
                    langs.append(choice)
                    i += 1
            
            print(string)
            langs.append("en")
            print("en", end="")
            for i in range(len(langs) - 1):
                src = langs[i]
                dest = langs[i+1]
                print(f" => {dest}", end="")
                translation = translator.translate(translated, src=src, dest=dest)

                if translation.extra_data["possible-translations"] is None:
                    translated = translation.text
                    continue

                sentences = []
                for tl in translation.extra_data["possible-translations"]:
                    #print(tl[2])
                    sent = random.choice(tl[2])[0]
                    #print(sent)
                    sentences.append(sent)
                    pass
                #print(sentences)

                #print(translation.extra_data["possible-translations"])
                #translated = translation.text
                translated = " ".join(sentences)
            print("")

            if re.sub("\W", "", string).lower() == re.sub("\W", "", translated).lower():
                print(translated)
                raise(Exception("Too accurate!"))
            break
        except Exception as e:
            print("")
            print(f"Encoutered error: {e}")
            if (retry_count >= 20):
                print("Too many errors!")
                raise(e)
            print("Retrying in 3...")
            sleep(3)
            retry_count += 1
            continue
    return translated

#for i in search_subfolders("out"):
#    skip_files.append(re.sub("^.*?out[\\\\/]+", "", i))

start()

#print(escapes)
#with open("escapes.txt", "w") as o:
#    o.write("\n".join(escapes))

#files_info = {}
#for path in paths:
#    for file in search_subfolders(path):
#        if not file.endswith("binE"):
#            continue
#
#        with open(file, "rb") as o:
#            bin = o.read()
#        
#        binE = BinE(bin)
#
#        if len(binE.strings) < 1:
#            print(f"{file}: No strings")
#            continue
#        else:
#            print(f"{file}: {binE.strings[0]}")
#
#        file_info = {}
#        file_info["header"] = list(binE.header)
#
#        tuples = []
#        for i in binE.strings:
#            t = (i, True)
#            tuples.append(t)
#
#        file_info["strings"] = tuples
#
#        
#        with open(f"{file}.json", "w") as o:
#            json.dump(file_info, o)
#        #os.remove(file)
# 
#        files_info[file] = file_info

#with open("strings.json", "w") as o:
#    json.dump(files_info, o)

#inp = input("Input: ")
#print("X: " + translate_entry(inp, dont_dic=True))
#for language in languages:
#    if language == "en":
#        continue
#    t = translator.translate(f"Please try to receive {inp} before you leave.", src="en", dest=language)
#    print(f"en -> {language}")
#    for i in t.extra_data["possible-translations"]:
#        #print(f"{i[2]} ({i[0]})")
#        for pt in i[2]:
#            x = re.search(inp.replace("[", "[\[【]\s*").replace("]", "\s*[\]】]"), pt[0])
#            print(f"{pt[0]}, {x is not None}")
#            if x is None:
#                raise(Exception())
#    print("")
#    