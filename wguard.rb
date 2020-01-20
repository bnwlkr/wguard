class Wguard < Formula
  desc "Easily Block Websites on Mac"
  homepage "https://github.com/bnwlkr/wguard"
  url "https://github.com/bnwlkr/wguard/archive/v0.1.2.tar.gz"
  sha256 "20fa8a77831921bb639fa325399d316e3d5290a6e1f2621d6d6472d44e2f5ce7"


  def install
    bin.install "wguard.py" => "wguard"
  end

  test do
    system bin/"wguard", "-h"
  end
end
