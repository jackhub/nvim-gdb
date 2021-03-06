'''BashDB specifics.'''

import re
from gdb.parser import Parser


class BashDBParser(Parser):
    '''BashDB FSM.'''

    def __init__(self, common, cursor, win):
        super().__init__(common, cursor, win)

        re_jump = re.compile(r'[\r\n]\(([^:]+):(\d+)\):(?=[\r\n])')
        re_prompt = re.compile(r'[\r\n]bashdb<\(?\d+\)?> $')
        re_term = re.compile(r'[\r\n]Debugged program terminated ')
        self.add_trans(self.paused, re_jump, self._paused_jump)
        self.add_trans(self.paused, re_prompt, self._query_b)
        self.add_trans(self.paused, re_term, self._handle_terminated)
        self.state = self.paused

        self.command_map = {
            'delete_breakpoints': 'delete',
            'breakpoint': 'break'
        }

    def _handle_terminated(self, _):
        self.cursor.hide()
        return self.paused
