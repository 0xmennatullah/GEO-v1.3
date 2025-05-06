let
  unstable = import (fetchTarball https://nixos.org/channels/nixos-unstable/nixexprs.tar.xz) { };
in
{ pkgs ? (import <nixpkgs> {}) }:
with pkgs;
  mkShell {
  packages = [ #These are only specific to NixOS because it doesn't provide it at runtime

  ];

  buildInputs = with pkgs; [ # Required packages for build
    ffmpeg
    unstable.python313
    unstable.python313Packages.numpy
    unstable.python313Packages.manim
    unstable.python313Packages.tkinter
    unstable.texliveFull

  ];
  # Specific to NixOS
  LD_LIBRARY_PATH = "${unstable.stdenv.cc.cc.lib}/lib";
}

