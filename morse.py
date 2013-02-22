import sublime, sublime_plugin, string

char_code_map = {
	"a": ".-",    "b": "-...",  "c": "-.-.",  "d": "-..",
	"e": ".",     "f": "..-.",  "g": "--.",   "h": "....",
	"i": "..",    "j": ".---",  "k": "-.-",   "l": ".-..",
	"m": "--",    "n": "-.",    "o": "---",   "p": ".--.",
	"q": "--.-",  "r": ".-.",   "s": "...",   "t": "-",
	"u": "..-",   "v": "...-",  "w": ".--",   "x": "-..-",
	"y": "-.--",  "z": "--..",  " ": " ",

	"1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
	"6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----",

	".": ".-.-.-", ",": "--..--", "?": "..--..",  "'": ".----.",
	"/": "-..-.",  "(": "-.--.",  ")": "-.--.-",  "&": ".-...",
	":": "---...", ";": "-.-.-.", "=": "-...-",   "+": ".-.-.",
	"-": "-....-", "_": "..--.-", "\"": ".-..-.", "$": "...-..-",
	"!": "-.-.--", "@": ".--.-."
}

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
		original = self.view.substr(currentSelection)
		original_lower = string.lower(original)
		output, prev_char = "", " "
		invalid_char_found = False

		def get_code_of_non_whitespace(char, prev_char):
			def get_code(char):
				try:
					code = char_code_map[char]
					return code
				except KeyError:
					invalid_char_found = True

				return None

			code = get_code(char)
			if code is None:
				return ""

			result = ""
			if prev_char != " ":
				result += " "
			result += code

			return result

		for char in original_lower:
			if char == " ":
				if prev_char == char:
					continue

				output += " / "
			else:
				output += get_code_of_non_whitespace(char, prev_char)

			prev_char = char

		if invalid_char_found:
			print "invalid characters found and ignored."

		self.view.replace(edit, currentSelection, output)

		return sublime.Region(currentSelection.begin(), currentSelection.begin() + len(output))