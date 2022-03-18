# encoding: utf-8
"""
    Rpy游戏的基本元素
"""
from corelib.exception import RenderException
from model import RpyElement

ROLE_TEMPLATE = "define {name} = Character('{role}', color=\"{color}\", image=\"{side_character}\")"  # 角色模板


# 对话
class Text(RpyElement):

    def __init__(self, text, role, triggers=None):
        """
        :param text: 文本
        :param role: 角色
        @:param triggers: 触发器：背景、音乐等等改变
        """
        self.text = text
        self.role = role
        self.triggers = triggers or list()

    def render(self, mode='nvl'):
        # result = [t.render() for t in self.triggers]
        result = []
        if self.role:
            result.append("{character} {text}".format(character=self.role.pronoun, text="\"{}\"".format(self.text)))
        elif mode == 'nvl':
            result.append("{character} {text}".format(character="narrator_nvl", text="\"{}\"".format(self.text)))
        elif mode == 'adv':
            result.append("{character} {text}".format(character="narrator_adv", text="\"{}\"".format(self.text)))
        return "\n".join(result)

    def add_triggers(self, *triggers):
        if not self.triggers:
            self.triggers = triggers
        else:
            self.triggers += triggers


class Role(RpyElement):
    pass
#     def __init__(self, pronoun, name, color=None):
#         """
#         :param pronoun: 代称
#         :param name: 角色名
#         :param color: 颜色
#         """
#         self.pronoun = pronoun
#         self.name = name
#         self.color = color or "#c8c8ff"

#     def render(self):
#         if not self.name:
#             return ""
#         return ROLE_TEMPLATE.format(name=self.pronoun, role=self.name, color=self.color, side_character=self.pronoun)


class Image(RpyElement):

    def __init__(self, name, cmd, position=""):
        self.name = name
        self.cmd = cmd
        self.position = position

    def hide(self):
        if not self.name:
            return ""
        else:
            return "    hide {name}".format(name=self.name)

    def scene(self):
        return "    scene {name}".format(name=self.name)

    def show(self):
        if self.position:
            return "    show {name} at {position}".format(name=self.name, position=self.position)
        else:
            return "    show {name}".format(name=self.name)

    def render(self):
        if self.cmd == 'show':
            return self.show()
        elif self.cmd == 'scene':
            return self.scene()
        elif self.cmd == 'hide':
            return self.hide()
        else:
            raise RenderException("Invalid Image Command:{}".format(self.cmd))


class Transition(RpyElement):

    def __init__(self, style):
        """
        :param style: 转场效果：dissolve (溶解)、fade (褪色)、None (标识一个特殊转场效果,不产生任何特使效果)
        """
        self.style = style

    def render(self):
        return "    with {}".format(self.style) if self.style else ""



class Mode(RpyElement):

    def __init__(self, mode):
        self.mode = mode

    def render(self):
        if self.mode in ['nvl', 'adv']:
            return ''
        else:
            return 'nvl clear'


class Voice(RpyElement):
    def __init__(self, name, sustain=False):
        self.name = "audio/voice/" + name
        self.sustain = sustain
        
        # sustain not implement

    def render(self):
        return '    voice "{}"'.format(self.name)


class Menu(RpyElement):
    def __init__(self, label, target):
        self.label = label
        self.target = target


class Option(RpyElement):
    def __init__(self, play_through_required):
        self.play_through_required = play_through_required

    def render(self, text):
        if self.play_through_required:
            return "        \"{option}\" if persistent.en > 0:\n".format(option=text)
        else:
            return "        \"{option}\":\n".format(option=text)
    

# 自定义指令
class Command(RpyElement):
    def __init__(self, cmd):
        self.cmd = cmd

    def render(self):
        return self.cmd
    

class AddRomance(RpyElement):
    def __init__(self, character, romance_point):
        self.character = character
        self.romance_point = romance_point
        
    def render(self):
        return "    $ " + "romance_point_{char_var} += {romance_point}".format(char_var=self.character, romance_point=self.romance_point)
    

class IfRomance(RpyElement):
    def __init__(self, character, condition, compare_value_1, compare_value_2):
        self.character = character
        self.condition = condition
        self.compare_value_1 = compare_value_1
        self.compare_value_2 = compare_value_2
        
    def render(self):
        if not self.compare_value_2 and self.condition != 'InRange':
            return "    if " + "romance_point_{char_var} {condition} {compare_value_1}:".format(char_var=self.character, condition=self.condition, compare_value_1=self.compare_value_1)
        else:
            return "    if " + "romance_point_{char_var} >= {compare_value_1} and romance_point_{char_var} <= {compare_value_2}:".format(char_var=self.character, compare_value_1=self.compare_value_1, compare_value_2 = self.compare_value_2)
            

# key class
class Dialog(RpyElement):

    def __init__(self, text, character, style):
        self.text = text
        self.character = character
        self.style = style

    def render(self):
        result = []
        transition_str = ""
        if self.character:
            dialog_text = "    {character} \"{text}\"".format(character=self.character, text=self.text)
        if self.style:
            transition_str = " with {}".format(self.style) if self.style else ""
        result_str = dialog_text + transition_str
        result.append(result_str)
        return "\n".join(result)


class Audio(RpyElement):

    def __init__(self, name, cmd, **args):
        """
        :param name: 音效名
        :param cmd: 指令
        :param args: 参数 fadeout/fadein: 音乐的淡入淡出  next_audio:下一个音效
        """
        self.cmd = cmd
        if isinstance(name, float):
            self.name = str(int(name))
        elif isinstance(name, int):
            self.name = str(name)
        else:
            self.name = name
        if self.name.split(".")[-1].lower() != 'mp3':
            self.name += ".mp3"
        
        if cmd == 'sound' or cmd == 'loop':
            self.name = "audio/sfx/" + self.name
        else:
            self.name = "audio/music/" + self.name
        self.fadeout = args.get("fadeout", 0.5)
        self.fadein = args.get("fadein", 0.5)
        self.next_audio = args.get("next_audio")

    def play(self):
        return "    play music \"{}\"".format(self.name)

    def fade(self):
        return self.play() + "fadeout {fadeout} fadein {fadein}".format(fadeout=self.fadeout, fadein=self.fadein)

    def queue(self):
        if self.next_audio:
            return "    queue \"{audio_name}\"".format(audio_name=self.next_audio.name)
        else:
            return self.play()

    def sound(self):
        return "    play sound \"{}\"".format(self.name)

    def loop(self):
        return self.sound() + " loop"

    def stop_music(self):
        return "    stop music"

    def stop_sound(self):
        return "    stop sound"

    def render(self):
        if self.cmd == 'play':
            return self.play()
        elif self.cmd == 'fade':
            return self.fade()
        elif self.cmd == 'queue':
            return self.queue()
        elif self.cmd == 'sound':
            return self.sound()
        elif self.cmd == 'stop_music':
            return self.stop_music()
        elif self.cmd == 'stop_sound':
            return self.stop_sound()
        elif self.cmd == 'loop':
            return self.loop()
        else:
            raise RenderException("Invalid Audio Command:{}".format(self.cmd))