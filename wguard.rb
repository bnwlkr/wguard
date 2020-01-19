class Wguard < Formula
	desc "Easily block access to websites on Mac and Linux"
	homepage "https://github.com/bnwlkr/wguard"
	version "0.1.0"
	url "https://github.com/bnwlkr/wguard/archive/0.1.0.tar.gz"
	
	
	def install
		bin.install "wguard.py" => "wguard"
	end
end
