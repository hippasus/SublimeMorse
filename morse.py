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

word_separator_code = " / "

class MorseCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		newSelections = []

		edit = self.view.begin_edit('morse')

		for currentSelection in self.view.sel():
			newSelections.append(self.convert_to_morse_code(edit, currentSelection))

		self.view.sel().clear()

		for newSelection in newSelections:
			self.view.sel().add(newSelection)

		self.view.end_edit(edit)

	def convert_to_morse_code(self, edit, currentSelection):
		line_ending = self._get_line_ending()
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
			for char in word:
				coded_char, ok = get_coded_char(char)
				coded_word += coded_char
				if ok:
					coded_word += " "
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

	def _get_line_ending(self):
		line_ending_setting = self.view.settings().get('default_line_ending')
		if line_ending_setting == 'windows':
			return '\r\n'
		elif line_ending_setting == 'mac':
			return '\r'
		return '\n'

	def normalize_line_endings(self, string):
		string = string.replace('\r\n', '\n').replace('\r', '\n')
		line_ending = self._get_line_ending()
		string = string.replace('\n', line_ending)
		return string
