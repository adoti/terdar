import math

def round_d(number:float, decimals:int=2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor

class Trade:
	_taker_fee = 0.0007
	_maker_fee = 0.0002

	def __init__(self):
		self.entry = 0
		self.target = 0
		self.exit = 0
		self.risk = 0
		self.direction = None

	def update(self):
		pass
	
	def print_all(self):
		print({"entry": self.entry, "target": self.target, "exit": self.exit, "risk": self.risk, "direction": self.direction})

	def update_target(self,x):
		self.target = x

	def update_exit(self, x):
		self.exit = x

	def update_entry(self, x):
		self.entry = x

	def update_risk(self, x):
		self.risk = -x

	def check_step(self):
		return all(i for i in [self.entry,self.target,self.exit,self.risk])

	#risk is defined as a % of the bankroll to be risked. we can double check it though.
	def set_dir(self):
		if self.check_step():
			if self.entry > self.exit:
				self.direction = "LONG"
			else:
				self.direction = "SHORT"

	def get_dir(self):
		return self.direction

	def get_rr(self):
		if self.check_step():
			return round_d(-1*self.target_return()/self.exit_return(),4)

	def get_position_size(self):
		if self.check_step():
			if self.get_dir() == "LONG":
				return round_d(self.risk/(self.exit - self.entry - self.market_fee(self.exit) - self.market_fee(self.entry)),4)
			else:
				return round_d(self.risk/(self.entry - self.exit - self.market_fee(self.exit) - self.market_fee(self.entry)),4)

		# if entry_usd > exit_usd: #the trade is LONG
		# 	return ("Long",round(target_risk_usd/(exit_usd - entry_usd - market_fee(entry_usd) - market_fee(exit_usd)),4))
		# else: #the trade is SHORT
		# 	return ("Short",round(target_risk_usd/(entry_usd - exit_usd - market_fee(entry_usd) - market_fee(exit_usd)),4))

	def target_return(self):
		if self.check_step():
			if self.get_dir() == "LONG":
				return round_d(self.get_position_size() * (self.target - self.entry - self.limit_fee(self.target) - self.market_fee(self.entry)),4)
			else:
				return round_d(self.get_position_size() * (self.entry - self.target - self.limit_fee(self.target) - self.market_fee(self.entry)),4)

	#aka get actual risk
	def exit_return(self):
		if self.check_step():
			if self.get_dir() == "LONG":
				return round_d(self.get_position_size() * (self.exit - self.entry - self.limit_fee(self.exit) - self.market_fee(self.entry)),4)
			else:
				return round_d(self.get_position_size() * (self.entry - self.exit - self.limit_fee(self.exit) - self.market_fee(self.entry)),4)

	def market_fee(self, price):
		return price * self._taker_fee

	def limit_fee(self, price):
		return price * self._maker_fee

	#assumes risk = negative number
	def get_position_size(self):
		if self.check_step():
			if self.direction:
				if self.direction == "LONG":
					return round_d(self.risk/(self.exit - self.entry - self.market_fee(self.exit) - self.market_fee(self.entry)),4)
				else:
					return round_d(self.risk/(self.entry - self.exit - self.market_fee(self.exit) - self.market_fee(self.entry)),4)
			return None
		# if entry_usd > exit_usd: #the trade is LONG
		# 	return ("Long",round(target_risk_usd/(exit_usd - entry_usd - market_fee(entry_usd) - market_fee(exit_usd)),4))
		# else: #the trade is SHORT
		# 	return ("Short",round(target_risk_usd/(entry_usd - exit_usd - market_fee(entry_usd) - market_fee(exit_usd)),4))

if __name__ == "__main__":

	trade = Trade(5900,6000,5800,-3.30)

	print(trade.get_position_size())
	print(trade.get_dir())
	print(trade.target_return())
	print(trade.exit_return())
	print(trade.get_rr())
	print()

	trade.update(5900,5800,6000,-3.30)

	print(trade.get_position_size())
	print(trade.get_dir())
	print(trade.target_return())
	print(trade.exit_return())
	print(trade.get_rr())
	
	#print("short risk = $3.30 entry = 5900, exit = 6000")
	#print(get_position_size(-3.3,5900,6000))
	#print("long risk = $3.30 entry = 5900, exit = 5800")
	#print(get_position_size(-3.3,5900,5800))