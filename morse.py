#!/usr/bin/python
# -*- coding: utf-8 -*-

import sublime, sublime_plugin, string

char_code_map = {
	"a": ".-",		"b": "-...",	"c": "-.-.",	"d": "-..",
	"e": ".",		"f": "..-.",	"g": "--.",		"h": "....",
	"i": "..",		"j": ".---",	"k": "-.-",		"l": ".-..",
	"m": "--",		"n": "-.",		"o": "---",		"p": ".--.",
	"q": "--.-",	"r": ".-.",		"s": "...",		"t": "-",
	"u": "..-",		"v": "...-",	"w": ".--",		"x": "-..-",
	"y": "-.--",	"z": "--..",	" ": " ",

	"1": ".----",	"2": "..---",	"3": "...--",	"4": "....-",	"5": ".....",
	"6": "-....",	"7": "--...",	"8": "---..",	"9": "----.",	"0": "-----",

	".": ".-.-.-",	",": "--..--",	"?": "..--..",	"'": ".----.",
	"/": "-..-.",	"(": "-.--.",	")": "-.--.-",	"&": ".-...",
	":": "---...",	";": "-.-.-.",	"=": "-...-",	"+": ".-.-.",
	"-": "-....-",	"_": "..--.-",	"\"": ".-..-.",	"$": "...-..-",
	"!": "-.-.--",	"@": ".--.-."
}

code_char_map = {}

word_separator_code = " / "

def _get_line_ending(view):
	line_ending_setting = view.settings().get('default_line_ending')
	if line_ending_setting == 'windows':
		return '\r\n'
	elif line_ending_setting == 'mac':
		return '\r'
	return '\n'

def _get_key_by_match_value(dict, v):
	for k in dict.keys():
		if v == dict[k]:
			return k
	return None

class MorseEncodeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		newSelections = []

		edit = self.view.begin_edit('morse_encode')

		for currentSelection in self.view.sel():
			newSelections.append(self.convert_to_morse_code(edit, currentSelection))

		self.view.sel().clear()

		for newSelection in newSelections:
			self.view.sel().add(newSelection)

		self.view.end_edit(edit)

	def convert_to_morse_code(self, edit, currentSelection):
		line_ending = _get_line_ending(self.view)
		invalid_char_found = False

		def get_coded_selection():
			text = self.view.substr(currentSelection)
			return get_coded_text(text)

		def get_coded_text(text):
			text_lower = string.lower(text)
			lines = text_lower.split(line_ending)
			result = get_coded_lines(lines)
			return result

		def get_coded_lines(lines):
			l, coded_lines = len(lines), ""

			for line in lines:
				coded_lines += get_coded_line(line)
				coded_lines += line_ending
			if l > 0:
				coded_lines = coded_lines[:-len(line_ending)]
			return coded_lines

		def get_coded_line(line):
			words = line.split()
			l, coded_line = len(words), ""

			for word in words:
				coded_line += get_coded_word(word)
				coded_line += word_separator_code
			if l > 0:
				coded_line = coded_line[:-len(word_separator_code)]
			return coded_line

		def get_coded_word(word):
			coded_word = ""
			prev_ok = True
			for char in word:
				coded_char, ok = get_coded_char(char)
				if ok:
					coded_char += " "
					if not prev_ok:
						coded_char = " " + coded_char

				coded_word += coded_char
				prev_ok = ok

			coded_word = coded_word.strip()
			return coded_word

		def get_coded_char(char):
			try:
				code = char_code_map[char]
				return code, True
			except KeyError:
				invalid_char_found = True
			return char, False

		output = get_coded_selection()

		if invalid_char_found:
			print "invalid characters found and ignored."

		self.view.replace(edit, currentSelection, output)

		return sublime.Region(currentSelection.begin(), currentSelection.begin() + len(output))

class MorseDecodeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		newSelections = []

		edit = self.view.begin_edit('morse_decode')

		for currentSelection in self.view.sel():
			newSelections.append(self.convert_to_text(edit, currentSelection))

		self.view.sel().clear()

		for newSelection in newSelections:
			self.view.sel().add(newSelection)

		self.view.end_edit(edit)

	def convert_to_text(self, edit, currentSelection):
		line_ending = _get_line_ending(self.view)
		invalid_code_found = False

		def decode_selection():
			text = self.view.substr(currentSelection)
			return decode_text(text)

		def decode_text(text):
			lines = text.split(line_ending)
			return decode_lines(lines)

		def decode_lines(lines):
			l, decoded_lines = len(lines), ""

			for line in lines:
				decoded_lines += decode_line(line)
				decoded_lines += line_ending
			if l > 0:
				decoded_lines = decoded_lines[:-len(line_ending)]
			return decoded_lines

		def decode_line(line):
			words = line.split(word_separator_code)
			l, decoded_line = len(words), ""

			for word in words:
				decoded_line += decode_word(word)
				decoded_line += " "
			if l > 0:
				decoded_line = decoded_line[:-1]
			return decoded_line

		def decode_word(word_codes):
			characters = word_codes.split()
			decoded_word = ""
			for char in characters:
				decoded_word += decode_char(char)
			return decoded_word

		def decode_char(char_code):
			char_code_lower = string.lower(char_code)
			try:
				char = code_char_map[char_code_lower]
			except KeyError:
				char = _get_key_by_match_value(char_code_map, char_code_lower)
				if char is None:
					invalid_code_found = True
					return char_code
				else:
					code_char_map[char_code_lower] = char

			return char

		output = decode_selection()

		if invalid_code_found:
			print "invalid Morse code found and ignored."

		self.view.replace(edit, currentSelection, output)

		return sublime.Region(currentSelection.begin(), currentSelection.begin() + len(output))
