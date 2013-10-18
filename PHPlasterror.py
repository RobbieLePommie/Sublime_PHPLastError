# Sublime 2 Package
# Will go to file and line of last error as logged in PHP error.log
# (C) 2013 Rob Spriggs
#

import re
import os
import sublime
import sublime_plugin


class phplasterrorCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        #sublime.status_message("Yay")
        settings_file = 'PHPlasterror.sublime-settings'
        settings = sublime.load_settings(settings_file)
        if settings.has('php_error_log'):
            log_file = settings.get('php_error_log')
            if os.path.exists(log_file):
                # Open the file and read the last line
                with open(log_file, "r") as f:

                    if settings.has('num_byes_to_read'):
                        num_bytes = settings.get('num_byes_to_read')
                    else:
                        num_bytes = 2048

                    f.seek(0, 2)           # Seek @ EOF
                    fsize = f.tell()        # Get Size
                    f.seek(max(fsize-num_bytes, 0), 0)    # Set pos @ last n chars
                    lines = f.readlines()     # Read to end
                    file_name = False
                    first_line = 'Empty File'
                    reading_line = -1
                    sublime.status_message('line ' + str(reading_line))
                    hasError = 0;
                    inTrace = 0;

                    while reading_line > 0 - len(lines) and lines[reading_line] and not hasError:
                        sublime.status_message('line ' + str(reading_line))
                        line = lines[reading_line]  # Get last Line
                        if reading_line == -1:
                            first_line = line

                        matchObj = re.match('\[(.*)\] (.*)', line)
                        if matchObj:
                            error = matchObj.group(2)
                            if error[:2] == '- ':     # Fat Free Error Logs
                                matchObj2 = re.match('(.*?):([0-9]*) .*', error[2:])
                                if matchObj2:
                                    inTrace = 1
                                    file_name = matchObj2.group(1)
                                    line_num = matchObj2.group(2)

                            elif inTrace:
                                hasError=1	#Get out, using this line as the error message

                            else :
                                matchObj2 = re.match('(.*) in (.*) on line (.*)', error)
                                if matchObj2:
                                    error = matchObj2.group(1)
                                    file_name = matchObj2.group(2)
                                    line_num = matchObj2.group(3)
                                    hasError = 1;

                        reading_line = reading_line - 1

                    if file_name:
                        if os.path.exists(file_name):
                            self.view.window().open_file(file_name + ':' + line_num, sublime.ENCODED_POSITION)
                            sublime.status_message(error + ' on line ' + line_num)
                        else:
                            sublime.status_message(error + ' on line ' + line_num + ' ** File ' + file_name + ' not found **')
                    else:
                        sublime.status_message('Unknown error message ' + first_line)
            else:
                sublime.status_message('Error log not found at ' + log_file)
        else:
            sublime.status_message('Log file not set')
