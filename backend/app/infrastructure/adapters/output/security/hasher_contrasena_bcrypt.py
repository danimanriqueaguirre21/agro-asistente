import bcrypt

from app.domain.ports.output.hasher_contrasena_port import PuertoHasherContrasena


class HasherContrasenaBcrypt(PuertoHasherContrasena):
    def hashear_contrasena(self, contrasena: str) -> str:
        hashed = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    def verificar_contrasena(self, contrasena: str, hash_contrasena: str) -> bool:
        return bcrypt.checkpw(
            contrasena.encode("utf-8"),
            hash_contrasena.encode("utf-8"),
        )
