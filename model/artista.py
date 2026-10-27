from dataclasses import dataclass, field


@dataclass
class Artista:
    ArtistId: int
    Name: str

    lista_brani: list = field(default_factory=list)
    lista_playlist: list = field(default_factory=list)




    def __hash__(self):
        return hash(self.ArtistId)

    def __str__(self):
        return f"{self.Name}"

    def __eq__(self, other):
        return self.ArtistId == other.ArtistId

    def numero_brani(self):
        lista = self.lista_brani
        return len(lista)