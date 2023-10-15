#!/usr/bin/env python

import sys
import string
import re
import copy
import traceback



# TODO:
#
#  TokenType priorities
#  action method chaining

debug_level=0
strict=False
#strict=True

def parse(pstring,initstate,tokentypes,data=None):
	tokens=Token.tokenize(pstring,tokentypes)
	state=initstate
	for token in tokens:
		debug('Calling state.process_token(%s,data) with state = %s' % (token,state),5)
		(state,data)=state.process_token(token,data)
	return (tokens,data)
	

def debug(msg,level=1):
	if debug_level >= level:
		sys.stderr.write(msg + '\n')



class TokenType:
	"""
		TokenType's represent kinds of Tokens. If you are parsing a 
		shell script, one token type, 'while', might represent the 
		beginning of a while loop.
		
		You can Register a new token type for parsing text, by
		Instantiating Token.Types like Token.Type(name,regex),
		for instance:

			Token.Type('eol','\n')
	"""
	auto_priority=0

	def __init__(self,name,regex):
		self.name = name
		self.regex=regex
		self.re = re.compile(regex)

	def match(self,string):
		"""
			This tests a string to see if it starts
			with text which is appropriate for this Token.Type.

			If so, it returns a Token of that text, and a 
			copy of the string with that text removed.

			If not, it returns None.
		"""
		m=self.re.match(string)
		if m :
			t=Token(self,m.group())
			st=string[len(t):]
			return (t,st)
		else:
			t=''
			return ('',string)

	def __repr__(self):
		return '<TokenType %s: %s>' % (repr(self.name),repr(self.regex))

# create a default token type to catch stuff that nothing else catches
TokenType.unmatched=TokenType(name='unmatched', regex='(?sL).')

class Token:
	"""
		Tokens represent meaningful chucks of text read from a string.
	"""

	def __init__(self,type,string):
		self.type=type
		self.string=string

	def __len__(self):
		return len(self.string)

	def tokenize(cls,mystring,tokentypes):
		"""
			Take a string, break it into tokens based on the known types (tokentypes),
			and returns a list of Tokens for the string.
		"""
		tokens=[] # the collection of tokens we have read
		mystring=copy.deepcopy(mystring)
		unmatched_type=TokenType.unmatched
		
		unmatched='' # the leading section of the mystring which doesn't match any known entity
		while mystring:
			# we have not tokenized all of mystring yet
			debug('###############################')
			token='' # the leading section of the mystring which matches the pattern for a known entity
			for ttype in tokentypes + [unmatched_type,]:
				debug('Trying to match "%s" on "%s..."' % (ttype.name,mystring[0:10]),2)
				(newtoken,newstring) = ttype.match(mystring)
				if newtoken: 
					debug('Matched!',2)
					token=newtoken
					mystring=newstring
					break
			debug('finaltoken="%s"' % token,3)
			if token.type == unmatched_type and tokens and (tokens[-1]).type == unmatched_type:
				# if this token is "unmatched" and the last one was too, just merge the data from 
				# this one into the last, so that we minimize the number of tokens
				(tokens[-1]).string += token.string
			else:
				tokens.append(token)
			debug('###############################')
		return tokens
	tokenize=classmethod(tokenize)

	def __repr__(self):
		return '<Token: %s (%s)>' % (repr(self.string),self.type.name)




class StateTransition:
	def __init__(self,token_type,from_state, to_state,action=[]):
		token_type_name=token_type.name
		if token_type.__class__ == TokenType:
			self.token_type=token_type
		else:
			raise 'Tried to create a state transition with an unknown token_type: "%s"' % token_type.name
		if from_state.__class__ == State:
			self.from_state=from_state
		else:
			raise 'Tried to create a state transition from an unknown state : "%s"' % from_state
		if to_state.__class__ == State or to_state == None: # allow to_state == None if transition calculates next state
			self.to_state=to_state
		else:
			raise 'Tried to create a state transition to an unknown state : "%s"' % to_state
		if action:
			self.action=action
		else:
			self.action = [lambda state,nextstate,token,data: (nextstate,data)]
	def __repr__(self):
		if self.to_state:	
			return '<StateTransition: %s -> %s if %s>' % (repr(self.from_state.name),repr(self.to_state.name),repr(self.token_type.name))
		else:
			return '<StateTransition: %s -> %s if %s>' % (repr(self.from_state.name),'None',repr(self.token_type.name))


class State:

	def __init__(self,name,transitions=[]):
		self.name = name
		self.transitions={}
		if strict and self.name != 'parse_error':
			def raise_error(state,next_state,token,data):
				if token.type.name=='unmatched':
					raise 'Parse Error: Found unmatched token "%s" in state "%s"' % (token,state)
			self.add_transition(TokenType.unmatched,parse_error_state,[raise_error,])

	def add_transition(self,token_type,to_state,action=[]):
		self.transitions[token_type.name]=StateTransition(token_type,self,to_state,action)

	def process_token(self,token,data=None):
		if token.type.name in self.transitions.keys():
			transition=self.transitions[token.type.name]
			debug('Following transition: %s' % transition )
			next_state=transition.to_state
			for act in transition.action:
				(next_state,data)=act(self,next_state,token,data)
			ret=(next_state,data)
		elif token.type.name == 'unmatched':
			debug('Not following transition for token type "%s"' % token.type.name )
			ret=(self,data)
		elif strict:
			raise '%s cannot process tokens of type "%s".' % (self,token.type)
		else:
			debug('Not following transition for token type "%s"' % token.type.name )
			ret=(self,data)
		return ret
			

	def __repr__(self):
		return '<State: %s>' % repr(self.name)
		
parse_error_state=State('parse_error')
init_state=State('init')
