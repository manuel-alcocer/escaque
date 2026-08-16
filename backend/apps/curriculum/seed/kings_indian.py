"""King's Indian Defence / Defensa India de Rey (E60–E99)."""

from .schema import ExerciseSpec, OpeningSpec, TheorySpec, VariationSpec

KID = ["d4", "Nf6", "c4", "g6", "Nc3", "Bg7"]
CLASSICAL = KID + ["e4", "d6", "Nf3", "O-O", "Be2", "e5"]

KINGS_INDIAN = OpeningSpec(
    slug="india-de-rey",
    name="Defensa India de Rey",
    alternative_names=["King's Indian Defence"],
    eco_range="E60-E99",
    colour="black",
    first_played="Sistematizada por Bronstein y Boleslavsky, años 1940",
    line=KID,
    tagline="Ceder el centro para reventarlo después: la defensa más agresiva contra 1.d4.",
    summary=(
        "Las negras dejan que las blancas ocupen el centro con peones y desarrollan detrás "
        "del fianchetto. Cuando el centro se cierra, los dos bandos atacan en flancos "
        "opuestos y la partida se convierte en una carrera de un solo carril."
    ),
    description="""
La India de Rey es la respuesta hipermoderna a 1.d4: en vez de disputar el centro con
peones, las negras lo dejan ocupar y lo atacan desde lejos con **...Cf6, ...g6 y ...Ag7**.
El alfil de g7 apunta a la casilla d4 desde la primera jugada y no deja de apuntar en toda
la partida.

## La estructura que define todo

Casi todas las partidas importantes pasan por lo mismo: las blancas montan peones en c4,
d4 y e4; las negras juegan **...d6 y ...e5**; las blancas cierran con **d5**. En cuanto el
centro se cierra, la posición dicta el plan de los dos bandos sin margen de duda:

- **Las blancas atacan en el flanco de dama**, donde tienen más espacio, con c4-c5 y la
  ruptura en b o c.
- **Las negras atacan en el flanco de rey**, con ...f5, ...f4, ...g5, ...g4, llevando
  todas las piezas hacia h3 y g3.

Nadie defiende. Las dos partidas se juegan a la vez en dos mitades distintas del tablero y
gana quien llegue primero. Por eso la India de Rey produce partidas tan desiguales: cuando
sale bien, sale espectacular; cuando sale mal, las blancas rompen en el flanco de dama
tres jugadas antes y no hay vuelta atrás.

## Lo que hay que aceptar para jugarla

Las negras tienen menos espacio durante toda la apertura y su alfil de casillas claras
suele ser malo. Si el ataque de flanco de rey no llega, esas desventajas siguen ahí en el
final. Es una apertura de convicción: no se juega a medias.
""".strip(),
    variations=[
        VariationSpec(
            slug="india-rey-clasica",
            name="Variante Clásica",
            eco="E90-E99",
            line=CLASSICAL + ["O-O", "Nc6", "d5", "Ne7"],
            tagline="La posición fundamental: centro cerrado y dos ataques en marcha.",
            is_main_line=True,
            difficulty=2,
            drill_plies=[6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            drill_difficulty=2,
            idea=(
                "Las negras provocan d5 con ...Cc6 y llevan el caballo a e7, desde donde "
                "apoya ...f5 y puede saltar a g6 o c8 según haga falta."
            ),
            description="""
Tras **7...Cc6** las blancas casi siempre juegan **8.d5**, porque mantener la tensión con
el caballo pinchando d4 es incómodo. Y ese es exactamente el objetivo negro: provocar el
cierre del centro en el momento que le conviene.

**8...Ce7** parece un retroceso y no lo es. Desde e7 el caballo:

- deja libre el peón de f para ...f5, que es la ruptura de toda la variante;
- puede ir a g6 para apoyar ...f4 y ...h5;
- no estorba en el flanco de dama, donde las negras no van a jugar nada.

Esta es la posición que hay que reconocer de un vistazo. Todo lo que sigue —Mar del Plata,
Bayoneta, Gligoric— son maneras distintas de disputarla.
""".strip(),
            theory=[
                TheorySpec(
                    title="Cuenta las jugadas, no las piezas",
                    kind="plan",
                    body=(
                        "Con el centro cerrado, la evaluación deja de ir de piezas buenas y "
                        "malas y pasa a ir de **velocidad**. Cuenta cuántas jugadas necesita "
                        "cada bando para abrir una línea contra el rey contrario. Si las "
                        "negras necesitan seis y las blancas cinco, las negras están perdiendo "
                        "aunque su posición parezca preciosa."
                    ),
                    line=CLASSICAL + ["O-O", "Nc6", "d5", "Ne7"],
                    highlight=["c5", "f5", "g4", "b5"],
                    orientation="black",
                ),
                TheorySpec(
                    title="El alfil de g7 espera su momento",
                    kind="idea",
                    body=(
                        "Mientras el peón de e5 esté clavado en su sitio, el alfil de g7 muerde "
                        "granito. No es un problema: está esperando a que la ruptura ...f5-f4 y "
                        "el avance ...e4 abran la diagonal a1-h8. Cuando eso pasa, suele decidir "
                        "la partida de una sola jugada."
                    ),
                    highlight=["g7", "d4", "b2"],
                    orientation="black",
                ),
            ],
        ),
        VariationSpec(
            slug="india-rey-mar-del-plata",
            name="Variante Mar del Plata",
            eco="E97-E99",
            parent="india-rey-clasica",
            line=CLASSICAL
            + [
                "O-O", "Nc6", "d5", "Ne7", "Ne1", "Nd7", "f3", "f5", "Bd2", "Nf6",
                "Rc1", "f4", "c5", "g5", "Nd3", "Ng6",
            ],
            tagline="La carrera pura: las blancas rompen en c5, las negras avanzan con g5-g4.",
            difficulty=4,
            drill_plies=[16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
            drill_difficulty=4,
            idea=(
                "Ataque de peones en flancos opuestos sin ninguna concesión defensiva. "
                "El primero que abra una línea decisiva gana."
            ),
            description="""
El nombre viene del torneo de Mar del Plata de 1953, y la variante es el manifiesto de la
India de Rey. Después de **9.Ce1 Cd7 10.f3 f5**, los dos bandos dejan de mirarse.

La secuencia negra es mecánica y hay que saberla de memoria: **...f5, ...f4, ...g5, ...g4**,
y después ...h5, ...Tf6-h6, ...Cf6-g6-h4. Todo va a la misma casilla: **h3 y g3**, delante
del rey blanco. Muchas partidas terminan con un sacrificio de pieza en una de las dos, y
el sacrificio no se calcula hasta el mate, se juega porque no hay defensa razonable.

Las blancas hacen lo mismo por el otro lado: **c5, Cd3, Tc1**, ruptura en c5xd6 o b4-b5,
y entrada por la columna c hacia c7.

Cuenta los tiempos y verás por qué es tan aguda: las blancas necesitan unas cinco jugadas
para abrir la columna c; las negras, unas seis para abrir el flanco de rey. Esa jugada de
diferencia es toda la teoría de la variante.
""".strip(),
            theory=[
                TheorySpec(
                    title="Por qué ...f4 antes que ...g5",
                    kind="plan",
                    body=(
                        "**...f4** cierra la diagonal del alfil blanco de c1 y fija el peón de "
                        "e4, pero sobre todo prepara ...g5-g4 sin que las blancas puedan "
                        "contestar con f3xg4 abriendo la columna f contra el propio rey negro. "
                        "El orden importa: ...g5 antes de ...f4 permite defensas que después no "
                        "existen."
                    ),
                    line=CLASSICAL
                    + ["O-O", "Nc6", "d5", "Ne7", "Ne1", "Nd7", "f3", "f5", "Bd2", "Nf6", "Rc1", "f4"],
                    highlight=["f4", "g5", "g4", "h3"],
                    orientation="black",
                ),
            ],
            exercises=[
                ExerciseSpec(
                    ref="india-rey-mdp-avance",
                    prompt=(
                        "Las blancas han jugado 12.Tc1 y preparan c5. Pon en marcha el ataque "
                        "negro con el orden correcto de peones."
                    ),
                    setup=CLASSICAL
                    + ["O-O", "Nc6", "d5", "Ne7", "Ne1", "Nd7", "f3", "f5", "Bd2", "Nf6", "Rc1"],
                    answer=["f4", "c5", "g5"],
                    kind="plan",
                    difficulty=3,
                    themes=["ataque de flanco", "estructura de peones"],
                    hint="Primero cierra la diagonal del alfil de c1, después avanza el peón de g.",
                    explanation=(
                        "**12...f4** y luego **13...g5** es el orden correcto. Invertirlo permite "
                        "a las blancas romper con f3xg4 en el momento equivocado y abrir la "
                        "columna f justo delante del rey negro."
                    ),
                ),
            ],
        ),
        VariationSpec(
            slug="india-rey-bayoneta",
            name="Ataque Bayoneta",
            eco="E97",
            parent="india-rey-clasica",
            line=CLASSICAL + ["O-O", "Nc6", "d5", "Ne7", "b4", "Nh5", "Re1", "f5"],
            tagline="9.b4: empezar el ataque de flanco de dama antes de colocar nada.",
            difficulty=4,
            drill_plies=[16, 17, 18, 19],
            drill_difficulty=4,
            idea=(
                "Las blancas se saltan la preparación lenta y avanzan ya. Ganan el tiempo "
                "que decide la carrera, a costa de dejar su posición menos armada."
            ),
            description="""
**9.b4** es la respuesta moderna a la Mar del Plata, y es puro pragmatismo: si la variante
es una carrera, corre desde la primera jugada. Kramnik la popularizó en los noventa y le
quitó a la India de Rey buena parte de su reputación.

Las negras responden **9...Ch5** apuntando a f4, y **10...f5** en cuanto pueden. La
diferencia con la Mar del Plata clásica es que aquí las blancas ya han ganado un tiempo, y
en una carrera de un tiempo eso es mucho.
""".strip(),
        ),
        VariationSpec(
            slug="india-rey-petrosian",
            name="Sistema Petrosian",
            eco="E92-E93",
            parent="india-rey-clasica",
            line=CLASSICAL + ["d5", "a5", "Bg5", "h6", "Bh4", "Na6"],
            tagline="7.d5 inmediato: cerrar el centro antes de que las negras se preparen.",
            difficulty=3,
            drill_plies=[12, 13, 14, 15, 16, 17],
            drill_difficulty=3,
            idea=(
                "Cerrar el centro sin dejar que las negras jueguen ...Cc6 primero. El "
                "caballo negro tiene que buscarse la vida por a6 o d7."
            ),
            description="""
Petrosian entendió la India de Rey mejor que casi nadie, y su solución fue profiláctica:
**7.d5** cierra el centro de inmediato, antes de que las negras hayan colocado el caballo
en c6 con tempo.

Las negras responden **7...a5**, fijando el flanco de dama para frenar el avance b4, y
llevan el caballo a a6 en vez de a c6. Es una versión más lenta y más posicional de la
India de Rey: menos sacrificios, más maniobras.
""".strip(),
            theory=[
                TheorySpec(
                    title="...a5 no es una jugada de ataque",
                    kind="idea",
                    body=(
                        "**7...a5** es profilaxis pura: frena b2-b4 y le da al caballo de a6 la "
                        "casilla c5, desde donde presiona e4 y d3. En la India de Rey moderna "
                        "las negras no siempre atacan; a veces sólo impiden que las blancas "
                        "empiecen."
                    ),
                    highlight=["a5", "b4", "c5", "a6"],
                    orientation="black",
                ),
            ],
        ),
        VariationSpec(
            slug="india-rey-gligoric",
            name="Variante Gligoric",
            eco="E92",
            parent="india-rey-clasica",
            line=CLASSICAL + ["Be3", "Ng4", "Bg5", "f6", "Bh4", "g5", "Bg3", "Nh6"],
            tagline="7.Ae3 Cg4: la persecución del alfil que define la variante.",
            difficulty=3,
            drill_plies=[12, 13, 14, 15, 16, 17, 18, 19],
            drill_difficulty=3,
            idea=(
                "Las negras ganan tiempos persiguiendo al alfil, pero debilitan su enroque "
                "con ...f6 y ...g5. El caballo acaba en h6, lejos de todo."
            ),
            description="""
**7.Ae3** desarrolla y vigila d4 y c5. La respuesta **7...Cg4** ataca el alfil y provoca
una secuencia forzada muy característica: **8.Ag5 f6 9.Ah4 g5 10.Ag3 Ch6**.

Cuenta lo que ha pasado: las negras han ganado tres tiempos empujando al alfil, y a cambio
tienen los peones de f6 y g5 fuera de sitio y un caballo en h6. No es malo ni bueno por sí
mismo: es un intercambio de tiempo por estructura, y quién sale ganando depende de si el
centro se abre o no.
""".strip(),
        ),
        VariationSpec(
            slug="india-rey-samisch",
            name="Sistema Sämisch",
            eco="E80-E89",
            line=KID + ["e4", "d6", "f3", "O-O", "Be3", "e5", "d5", "Nh5", "Qd2", "f5"],
            tagline="5.f3: apuntalar e4 con un peón y enrocar largo.",
            difficulty=4,
            drill_plies=[6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            drill_difficulty=3,
            idea=(
                "Las blancas defienden e4 sin usar piezas, lo que les deja jugar Ae3, Dd2 y "
                "enroque largo, con g4 y h4 después."
            ),
            description="""
El Sämisch es la respuesta más directa: **5.f3** defiende e4 con un peón, y eso lo cambia
todo. El caballo de g1 ya no tiene que ir a f3 y puede ir a e2, el alfil de c1 sale a e3
sin problemas y las blancas pueden enrocar largo y atacar con **g4 y h4**.

De repente los dos bandos atacan en el mismo flanco, y la India de Rey pierde su claridad
habitual. Las negras suelen buscar contrajuego con **...c6 y ...b5** en el flanco de dama,
o con el sacrificio **...b5** del Gambito Benkó-like, para abrir líneas antes de que llegue
el ataque blanco.

La pega del Sämisch es el tiempo: f3 no desarrolla nada. Si las negras consiguen abrir el
centro rápido, esa jugada de peón se echa mucho de menos.
""".strip(),
            theory=[
                TheorySpec(
                    title="Enroques opuestos cambian las reglas",
                    kind="plan",
                    body=(
                        "Con las blancas enrocadas largo y las negras cortas, cada avance de "
                        "peón es una jugada de ataque y ninguna es reversible. Aquí no se "
                        "maniobra: se cuenta. Abrir una columna contra el rey rival una jugada "
                        "antes vale más que cualquier ventaja posicional."
                    ),
                    highlight=["g4", "h4", "b5", "c6"],
                ),
            ],
        ),
        VariationSpec(
            slug="india-rey-cuatro-peones",
            name="Ataque de los Cuatro Peones",
            eco="E76-E79",
            line=KID + ["e4", "d6", "f4", "O-O", "Nf3", "c5", "d5", "e6", "Be2", "exd5", "cxd5"],
            tagline="5.f4: ocupar todo el centro y aceptar el riesgo.",
            difficulty=4,
            drill_plies=[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            drill_difficulty=4,
            idea=(
                "Cuatro peones en c4, d4, e4 y f4. Espacio máximo y flexibilidad mínima: "
                "si las negras golpean el centro a tiempo, la estructura se resquebraja."
            ),
            description="""
La versión más ambiciosa y la más arriesgada. Con **5.f4** las blancas ocupan el centro
entero, pero un centro de cuatro peones es una diana: cada uno de ellos necesita defensa y
ninguno puede retroceder.

Las negras golpean de inmediato con **6...c5**, y tras **7.d5 e6** el centro empieza a
abrirse en el peor momento para las blancas. La línea **8.Ae2 exd5 9.cxd5** deja una
estructura tipo Benoni donde el alfil de g7 por fin respira.

Es una variante que castiga la ignorancia por los dos lados: las blancas que no la
conozcan pierden el centro, y las negras que no la conozcan se ven aplastadas por e4-e5.
""".strip(),
            exercises=[
                ExerciseSpec(
                    ref="india-rey-cuatro-peones-golpe",
                    prompt=(
                        "Las blancas han montado los cuatro peones y acaban de jugar 6.Cf3. "
                        "Golpea el centro."
                    ),
                    setup=KID + ["e4", "d6", "f4", "O-O", "Nf3"],
                    answer=["c5", "d5", "e6"],
                    kind="plan",
                    difficulty=3,
                    themes=["golpe central", "estructura"],
                    hint="Ataca la base del centro con el peón que todavía no se ha movido.",
                    explanation=(
                        "**6...c5** ataca d4 justo cuando las blancas no pueden sostenerlo con "
                        "comodidad. Tras **7.d5 e6** las negras minan la cadena por el otro "
                        "extremo y abren la diagonal del alfil de g7. Esperar aquí es el error: "
                        "si las blancas consiguen jugar e5 con calma, las negras se quedan sin "
                        "espacio y sin plan."
                    ),
                ),
            ],
        ),
        VariationSpec(
            slug="india-rey-fianchetto",
            name="Variante del Fianchetto",
            eco="E60-E69",
            line=[
                "d4", "Nf6", "c4", "g6", "Nf3", "Bg7", "g3", "O-O", "Bg2", "d6",
                "O-O", "Nbd7", "Nc3", "e5", "e4", "c6",
            ],
            tagline="4.g3: neutralizar al alfil de g7 con otro alfil en la misma diagonal.",
            difficulty=3,
            drill_plies=[4, 6, 8, 10, 12, 13, 14, 15],
            drill_difficulty=3,
            idea=(
                "El alfil de g2 mira a la misma diagonal que el de g7 y anula su presión. "
                "Sin esa presión, el ataque de flanco de rey negro pierde fuerza."
            ),
            description="""
La respuesta más sólida y la que menos gusta a los jugadores de India de Rey. **4.g3 y
5.Ag2** ponen un alfil blanco en la diagonal larga, exactamente enfrente del de g7. Los
dos se anulan, y con ellos se va buena parte del veneno negro.

Además, el alfil de g2 defiende el rey blanco desde su casa, así que el ataque de peones
...f5-f4-g5-g4 se encuentra con una posición mucho mejor amueblada que en la Clásica.

Las negras suelen elegir un plan distinto: **...Cbd7, ...e5 y ...c6**, jugando por el
centro en vez de por el flanco. Es una India de Rey más tranquila, casi una partida de
maniobras.
""".strip(),
            theory=[
                TheorySpec(
                    title="Dos alfiles en la misma diagonal se cancelan",
                    kind="structure",
                    body=(
                        "El alfil de g7 vale lo que vale la diagonal a1-h8. Con un alfil blanco "
                        "en g2, esa diagonal deja de ser una autopista y pasa a ser un espejo. "
                        "Por eso, contra el fianchetto, las negras cambian de plan en vez de "
                        "insistir con el ataque de siempre."
                    ),
                    highlight=["g2", "g7", "d4", "e5"],
                ),
            ],
        ),
        VariationSpec(
            slug="india-rey-averbaj",
            name="Sistema Averbaj",
            eco="E73-E75",
            line=KID + ["e4", "d6", "Be2", "O-O", "Bg5", "c5", "d5", "e6"],
            tagline="6.Ag5: clavar el caballo antes de que las negras jueguen ...e5.",
            difficulty=3,
            drill_plies=[6, 7, 8, 9, 10, 11, 12, 13],
            drill_difficulty=3,
            idea=(
                "Impedir ...e5 con una clavada en lugar de con peones. Las negras cambian "
                "de plan y golpean con ...c5, entrando en estructuras Benoni."
            ),
            description="""
**6.Ag5** ataca el punto que sostiene la ruptura ...e5: con el caballo de f6 clavado, la
jugada pierde fuerza. Es una manera muy económica de sacar a las negras de su terreno.

La respuesta principal es **6...c5**, cambiando de plan por completo. Tras **7.d5 e6** la
partida entra en una estructura de Benoni Moderna, donde el juego negro va por la columna
e y el flanco de dama en vez de por el ataque al rey.

Es una buena variante para quien quiere jugar contra la India de Rey sin memorizar la
Mar del Plata entera.
""".strip(),
        ),
        VariationSpec(
            slug="india-rey-cambio",
            name="Variante del Cambio",
            eco="E92",
            parent="india-rey-clasica",
            line=CLASSICAL + ["dxe5", "dxe5", "Qxd8", "Rxd8"],
            tagline="7.dxe5: cambiar damas pronto y dejar la partida sin ataque.",
            difficulty=2,
            drill_plies=[12, 13, 14, 15],
            drill_difficulty=2,
            idea=(
                "Sin damas no hay ataque al rey, y la India de Rey pierde su razón de ser. "
                "Las negras juegan un final ligeramente peor pero muy defendible."
            ),
            description="""
La forma más simple de desactivar la India de Rey: **7.dxe5 dxe5 8.Dxd8 Txd8**. Sin damas
no hay mate, y el plan negro de ...f5-f4-g5-g4 se queda sin objetivo.

No es una refutación. Las negras están perfectamente bien en el final, con la maniobra
típica **...Cc6-d4** o **...c6 y ...Ae6** para igualar. Pero es un jarro de agua fría para
quien haya elegido la apertura buscando una partida agresiva, y muchas blancas la juegan
exactamente por eso.

Ojo con una cosa: la posición está equilibrada, pero no es inofensiva. Aquí abajo hay una
táctica que decide partidas de club constantemente.
""".strip(),
            exercises=[
                ExerciseSpec(
                    ref="india-rey-cambio-nxe5",
                    prompt=(
                        "Las blancas han jugado 9.Cxe5 creyendo que ganan un peón. Recupera "
                        "el material."
                    ),
                    setup=CLASSICAL + ["dxe5", "dxe5", "Qxd8", "Rxd8", "Nxe5"],
                    answer=["Nxe4", "Nxe4", "Bxe5"],
                    kind="tactic",
                    difficulty=3,
                    themes=["desviación", "diagonal larga", "táctica de apertura"],
                    hint="El caballo de e5 defiende algo. Quítale el defensor a e4 primero.",
                    explanation=(
                        "**9...Cxe4!** funciona porque el caballo de c3 está sobrecargado y "
                        "porque el alfil de g7 recupera en e5 en cuanto la diagonal se abre. "
                        "Tras 10.Cxe4 Axe5 el material está igualado y las negras tienen un "
                        "alfil excelente. Ésta es la razón por la que las blancas juegan 9.Ag5 "
                        "o 9.Cd5 en lugar de coger el peón."
                    ),
                ),
            ],
        ),
        VariationSpec(
            slug="india-rey-makogonov",
            name="Variante Makogonov",
            eco="E71",
            line=KID + ["e4", "d6", "h3", "O-O", "Bg5", "c5"],
            tagline="5.h3: una jugada de espera que le quita g4 a las negras para siempre.",
            difficulty=3,
            drill_plies=[6, 7, 8, 9, 10, 11],
            drill_difficulty=3,
            idea=(
                "Quitarle al caballo negro la casilla g4 y preparar Ae3 sin sufrir ...Cg4. "
                "Profilaxis antes que desarrollo."
            ),
            description="""
**5.h3** parece una pérdida de tiempo y es una de las jugadas más molestas de la India de
Rey moderna. Le quita a las negras el recurso ...Cg4, que es la base de la Variante
Gligoric, y prepara Ae3 sin ninguna incomodidad.

También deja abierta la opción de **g4** más adelante, ganando espacio en el flanco donde
las negras quieren atacar. Es la clase de jugada que no gana nada por sí sola pero hace
que el plan del rival funcione peor durante veinte jugadas.
""".strip(),
        ),
    ],
)
