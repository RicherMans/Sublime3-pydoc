import sublime
import sublime_plugin
import re
import os


def read_line(view, point):
    if (point >= view.size()):
        return

    next_line = view.line(point)
    return view.substr(next_line)


def writeSnipplet(view, content):
    view.run_command(
        'insert_snippet', {
            'contents': content
        }
    )


def getBlanks(length,spaces):
    if spaces:
    	return ' '*length
    else:
        return '\t'

def tabmarkCounter():
    counter = 0
    while True:
        counter += 1
        yield counter


def getCommentCharacters(line):
    '''
    Function: getCommentCharacters Definition:Returns the characters which initiated the comment
    either \'\'\' or """
    @param line
    '''
    return re.search('[^a-zA-Z\d\s]+', line).group(0)


def getBlankSpaces(line, spaces=False):
    '''
    Returns the amount of Tabs/whitespaces in the current line
    @param spaces : if True, it checks for whitespace , otherwise
    for tabs
    '''
    if spaces:
        return ' ' * len(re.search('^(\s*)', line).group(0))
    else:
        return '\t' * len(re.search('^(\t*)', line).group(0))


def searchForFunctionDefiniton(view, point, maxlines=3):
    """
    Searches for a function definition in python and returns
    """
    line = read_line(view, point)
    # Read the proceeding maxlines lines
    for i in range(maxlines):
        point -= len(line)
        line = read_line(view, point)
        search = re.search("def (.+)\((.*)\)", line)
        if search:
            funcname = search.group(1)
            args = search.group(2)

            # Function definition has no arguments, return the name and a dummy
            ret = [funcname, []]
            if not args:
                return ret
            # Check if we have default values for the args
            # Remove all whitespaces
            arguments = args.replace(" ", "").split(',')
            argtodefault = []
            for arg in arguments:
                k, *v = arg.split('=')
                argtodefault.append((k, v))
            return [funcname, argtodefault]


class PyDocCommand(sublime_plugin.TextCommand):


    def run(self, edit):
        syntax = (self.view.settings().get('syntax'))
        self.settings = self.view.settings()
        # Get the users/default indent setting
        # Check if we currently have set python as the language of choice
        # Plugin only works if python is chosen
        if "python" in syntax.lower():
            point = self.view.sel()[0].end()
            definition = searchForFunctionDefiniton(
                self.view, point, maxlines=3)
            self.parseSettings()
            curline = read_line(self.view, point)
            commentCharacters = getCommentCharacters(curline)
            # We did not find any definition, only do print a newline
            if not definition:
                writeSnipplet(self.view, os.linesep)
                return

            snipplet = self.generateSnippet(
                definition, commentCharacters)
            writeSnipplet(self.view, snipplet)

        return 0

    def parseSettings(self):
        settings = sublime.load_settings('DocPy.sublime-settings')
        self.autocomplete_parts = settings.get('autocomplete_parts')
        self.autocomplete_text = settings.get('autocomplete_text')

    def generateSnippet(self, funcdefargs, closingcomments):
        # We use a dummpy at the first list item so that the .join(out) will produce
        # one newline at the beginning of the docstring ( right after the ''')

        out = ['']
        functionname, *args = funcdefargs
        counter = tabmarkCounter()
        tabsorSpaces = self.view.settings().get(
                'translate_tabs_to_spaces')
        tabsize = self.view.settings().get('tab_size')
        # If we have a given indent setting, we use that many indents
        blankspaces = getBlanks(tabsize,tabsorSpaces)

        # out1= []
        # for setting in self.autocomplete_parts:
        #     cursetting = self.autocomplete_mapping[setting]
        #     cursetting.setup(counter,blankspaces,args[0])
        #     out1.append(cursetting.printsetting())
        # print (out1)
        self.autocomplete_text=False
        if self.autocomplete_text:
            docstr = '${%d:InsertHere}'
        else:
            docstr = '${%d}'

        if 'function' in self.autocomplete_parts:
            out.append(
                'Function: {}'.format(functionname))
        if 'summary' in self.autocomplete_parts:
            out.append('Summary: '+docstr%(next(counter)))
        if 'examples' in self.autocomplete_parts:
            out.append('Examples: '+docstr%(next(counter)))
        if 'attributes' in self.autocomplete_parts:
            if len(args[0])>0:
                out.append('Attributes: ')
            # if args is empty it is only a single list, but if it's nonempty it's a list of
            # of a list of tuples.
            # args is a list of a list, we only need the inner list
            for arg in args[0]:
                param, default = arg
                if default:
                    # default is a list only containing one item, but we somehow needed
                    # to indicate whaether a default is given or not
                    out.append(
                        "%s@param (%s) default=%s: "%(blankspaces,param, default[0])+docstr%(next(counter)))
                else:
                    out.append("%s@param (%s):"%(blankspaces,param) + docstr%(next(counter)))
        if 'returns' in self.autocomplete_parts:
            out.append('Returns:'+docstr%(next(counter)))
        # append the closing tags
        out.append('{}'.format(closingcomments))
        # Append the tabstops for the snipplet

        return os.linesep.join(out)
