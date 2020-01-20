class Wguard < Formula
  desc "Easily Block Websites on Mac"
  homepage "https://github.com/bnwlkr/wguard"
  url "https://github.com/bnwlkr/wguard/archive/v0.1.1.tar.gz"
  sha256 "e478c1d5fdd4cbfc0632bc09e07dd9b44b37c7d9d76e51e12758d9f301644c54"


  def install
    bin.install "wguard.py" => "wguard"
  end

  test do
    system bin/"wguard"
  end
end
