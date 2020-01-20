class Wguard < Formula
  desc "Easily Block Websites on macOS"
  homepage "https://github.com/bnwlkr/wguard"
  url "https://github.com/bnwlkr/wguard/archive/v0.1.3.tar.gz"
  sha256 "77dc8802e6ce9285e4dfb7e68bff54993b18195a335e56c42b84f53cbd016626"


  def install
    bin.install "wguard.py" => "wguard"
  end

  test do
    system bin/"wguard", "-h"
  end
end
