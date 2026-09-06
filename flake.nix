{
  description = "Chrimbus";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = {nixpkgs, ...}: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        go
        gopls
        nodejs
        pnpm
        python3
        typescript-language-server
      ];
      shellHook = ''
        export CHRIMBUS_API_KEY=dev
      '';
    };
  };
}
