%% bibliotheca-missel.cls — Charte de la Bibliotheque Catholique
%% VARIANTE IMPRIMEE « format missel » : 110 x 170 mm, recto-verso, cahier pique.
%% Meme police, memes couleurs, memes ornements que bibliotheca.cls ;
%% seuls le format, les marges (petit fond / grand fond) et le titre courant miroir changent.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{bibliotheca-missel}[2026/11/10 Bibliotheca Catholica - missel]
\LoadClass[10pt,twoside,openany]{book}

%% 1. FORMAT — 110 x 170, marges en miroir (fond = pli/agrafes, un peu plus large)
\RequirePackage[
  paperwidth=110mm, paperheight=170mm,
  top=13mm, bottom=14mm, inner=13mm, outer=11mm,
  headsep=4mm, footskip=7.5mm, headheight=14pt
]{geometry}

%% 2. COULEURS
\RequirePackage{xcolor}
\definecolor{rubrique}{RGB}{124,26,29}
\definecolor{encre}{RGB}{26,26,26}

%% 3. TYPOGRAPHIE
\RequirePackage{fontspec}
\defaultfontfeatures{Ligatures=TeX}
\newcommand{\bib@fontdir}{/usr/share/fonts/opentype/ebgaramond/}
\setmainfont{EBGaramond12-Regular.otf}[
  Path=\bib@fontdir, ItalicFont=EBGaramond12-Italic.otf, BoldFont=EBGaramond12-Bold.otf,
  SmallCapsFont=EBGaramondSC12-Regular.otf, SmallCapsFeatures={Letters=SmallCaps},
  Numbers=OldStyle]
\ifdefined\JARDINFONT
  \setmainfont{\JARDINFONT-latin-400-normal.ttf}[Path=./,ItalicFont=\JARDINFONT-latin-400-italic.ttf,BoldFont=\JARDINFONT-latin-400-normal.ttf,SmallCapsFont=\JARDINFONT-latin-400-normal.ttf]
\fi
\newfontfamily\ebgsymb{EBGaramond12-Regular.otf}[Path=\bib@fontdir]
\ifdefined\JARDINTITRE\newfontfamily\titrefont{\JARDINTITRE}[Path=./]\else\let\titrefont\relax\fi
\newfontfamily\petitescaps{EBGaramondSC12-Regular.otf}[Path=\bib@fontdir]
\RequirePackage{newunicodechar}
\newunicodechar{℟}{{\ebgsymb\upshape ℟}}\newunicodechar{℣}{{\ebgsymb\upshape ℣}}\newunicodechar{†}{{\ebgsymb\upshape †}}
\newunicodechar{ᵉ}{\textsuperscript{e}}\newunicodechar{ʳ}{\textsuperscript{r}}
\newfontfamily\chiffresalignes{EBGaramond12-Regular.otf}[Path=\bib@fontdir,Numbers=Lining]
\RequirePackage[french]{babel}
\frenchsetup{IndentFirst=true}
\RequirePackage[protrusion=true,expansion=false,final]{microtype}
\frenchspacing
\renewcommand{\normalsize}{\fontsize{9.5}{11.7}\selectfont}
\setlength{\parindent}{1em}
\setlength{\emergencystretch}{1.5em}
\hyphenpenalty=200 \tolerance=2000
\widowpenalty=10000 \clubpenalty=10000 \brokenpenalty=10000
\raggedbottom
\setcounter{secnumdepth}{-1}
\AtBeginDocument{\color{encre}}

%% 4. ORNEMENTS
\RequirePackage{tikz}
\RequirePackage{pgfornament}
\RequirePackage{adjustbox}
%% Emblemes : un motif par priere, au-dessus du titre
\newcommand{\vignette}[2][9mm]{\adjustbox{max height=#1,max width=18mm}{\pgfornament[width=18mm,color=rubrique]{#2}}}
\newcommand{\bib@embleme}{\par\noindent\croix\par}
\newcommand{\embleme}[1]{\renewcommand{\bib@embleme}{\par\noindent#1\par}}
%% Croix latine (dessinee) : seul embleme de la collection, identique partout
\newcommand{\croix}[1][7mm]{\begin{tikzpicture}[x=#1/10,y=#1/10]
  \fill[rubrique] (-.45,0)--(.45,0)--(.45,6.45)--(2.3,6.45)--(2.3,7.35)--(.45,7.35)--(.45,10)--(-.45,10)
    --(-.45,7.35)--(-2.3,7.35)--(-2.3,6.45)--(-.45,6.45)--cycle;
\end{tikzpicture}}
%% Hostie rayonnante (dessinee)
\newcommand{\hostie}[1][9mm]{\begin{tikzpicture}[x=#1/20,y=#1/20,rubrique,line cap=round]
  \foreach \a in {0,15,...,345}{\draw[line width=.35pt] (\a:5.6)--(\a:9.8);}
  \foreach \a in {7.5,22.5,...,352.5}{\draw[line width=.25pt] (\a:5.6)--(\a:8);}
  \fill[white] (0,0) circle (5); \draw[line width=.7pt] (0,0) circle (5); \draw[line width=.3pt] (0,0) circle (4.3);
  \draw[line width=.8pt] (0,-2.6)--(0,2.6) (-1.7,.9)--(1.7,.9);
\end{tikzpicture}}
%% Monogramme IHS rayonnant (dessine)
\newcommand{\monogramme}[1][22mm]{\begin{tikzpicture}[x=#1/40,y=#1/40,rubrique,line cap=round]
  \foreach \a in {0,10,...,350}{\draw[line width=.4pt] (\a:11.5)--(\a:19.5);}
  \foreach \a in {5,15,...,355}{\draw[line width=.25pt] (\a:11.5)--(\a:16);}
  \draw[line width=.8pt] (0,0) circle (10.5); \draw[line width=.3pt] (0,0) circle (9.6);
  \node at (0,-.6) {\fontsize{12}{12}\selectfont\addfontfeature{LetterSpace=6}\textsc{ihs}};
  \draw[line width=.6pt] (.05,3.3)--(.05,7.4) (-1.4,6)--(1.5,6);
  \foreach \x in {-1.6,0.05,1.7}{\draw[line width=.5pt] (\x,-3.6)--(.05+.35*\x,-6.9);}
\end{tikzpicture}}
%% Cadre a coins graves
\newcommand{\cadre}{\begin{tikzpicture}[remember picture,overlay]
  \def\m{7mm}\def\w{17mm}
  \node[anchor=north west] at ([shift={(\m,-\m)}]current page.north west) {\pgfornament[width=\w,color=rubrique]{61}};
  \node[anchor=north east] at ([shift={(-\m,-\m)}]current page.north east) {\pgfornament[width=\w,color=rubrique,symmetry=v]{61}};
  \node[anchor=south west] at ([shift={(\m,\m)}]current page.south west) {\pgfornament[width=\w,color=rubrique,symmetry=h]{61}};
  \node[anchor=south east] at ([shift={(-\m,\m)}]current page.south east) {\pgfornament[width=\w,color=rubrique,symmetry=c]{61}};
\end{tikzpicture}}
\newcommand{\fleuron}[1][20mm]{\par\noindent\pgfornament[width=#1,color=rubrique]{88}\par}
\newcommand{\fleuronpetit}[1][11mm]{\par\noindent\pgfornament[width=#1,color=rubrique]{89}\par}
\RequirePackage{graphicx}
%% Fin de priere : ange heraut a la trompette (dessin vectoriel, bordeaux de la charte)
\newcommand{\culdelampe}[1][9mm]{\par
  \ifdim\dimexpr\pagegoal-\pagetotal\relax<\dimexpr#1+1.2\baselineskip\relax\else
  \nopagebreak[4]\vspace{.4\baselineskip}\nopagebreak[4]\noindent\includegraphics[height=#1]{angelot.pdf}\par\fi}
%% Frontispice : gloire a la croix entre deux anges herauts
\newcommand{\frontispice}{\thispagestyle{empty}\null\vfill\noindent\hfill\includegraphics[width=76mm]{gloire.pdf}\hfill\null\par\vspace*{6mm}\vfill\clearpage}
\newcommand{\filetdouble}{\par\noindent{\color{rubrique}\rule{\linewidth}{0.8pt}}\par\vspace{1mm}%
  \noindent{\color{rubrique}\rule{\linewidth}{0.3pt}}\par}

%% 5. LETTRINES — capitale EB Garamond ordinaire en bordeaux (jamais les Initials)
\RequirePackage{lettrine}
\renewcommand{\LettrineFontHook}{\color{rubrique}\titrefont}
\setcounter{DefaultLines}{2}
\setlength{\DefaultFindent}{1pt}
\setlength{\DefaultNindent}{0.3em}
\newcommand{\ouverture}[3]{\lettrine{#1}{#2}\ \textsc{#3}}

%% 6. TITRE COURANT MIROIR ET FOLIO EN PIED, cote exterieur
\RequirePackage{fancyhdr}
\RequirePackage{emptypage}
\newcommand{\bib@espace}[1]{{\petitescaps\fontsize{7.6}{9}\selectfont\addfontfeature{LetterSpace=8}#1}}
\fancypagestyle{bibliotheca}{\fancyhf{}\renewcommand{\headrulewidth}{0pt}
  \fancyhead[LE]{\bib@espace{\leftmark}}
  \fancyhead[RO]{\bib@espace{\rightmark}}
  \fancyfoot[LE,RO]{{\chiffresalignes\fontsize{8.6}{10}\selectfont\thepage}}}
\pagestyle{bibliotheca}
\renewcommand{\chaptermark}[1]{\markboth{#1}{#1}}
\renewcommand{\sectionmark}[1]{\markright{#1}}
\fancypagestyle{plain}{\fancyhf{}\renewcommand{\headrulewidth}{0pt}}
\fancypagestyle{ouverture}{\fancyhf{}\renewcommand{\headrulewidth}{0pt}%
  \fancyfoot[LE,RO]{{\chiffresalignes\fontsize{8.6}{10}\selectfont\thepage}}}

%% 7. TITRES — au fer a gauche (\filright = titre a gauche)
\RequirePackage{titlesec}
%% Pages de partie : composees a la main (recto, sans folio), entree de table
\newcommand{\partie}[3]{\clearpage\thispagestyle{ouverture}%
  \begingroup\raggedright\null\vspace*{1mm}\par
  \noindent\croix[9mm]\par\vspace{2.5mm}
  \bib@espace{#1}\par\vspace{2mm}
  {\fontsize{15}{18}\selectfont\titrefont\scshape\color{rubrique}#2\par}
  \vspace{2mm}{\color{rubrique}\rule{26mm}{0.5pt}}\par\vspace{5mm}\endgroup
  \markboth{#2}{}\addcontentsline{toc}{chapter}{#2}\bib@premier}
\newif\ifbib@apres \bib@apresfalse
\newcommand{\bib@premier}{\global\bib@apresfalse}
\titleformat{\section}[block]{\filright}{}{0pt}
  {\fontsize{11.2}{13.4}\selectfont\titrefont\scshape\color{rubrique}}[\vspace{1mm}{\color{rubrique}\rule{12mm}{0.4pt}}]
\titlespacing*{\section}{0pt}{2mm}{2.2mm}

%% 8. ELEMENTS DE PRIERE
%% invocation / conclusion : italique, au fer a gauche, sans alinea
\newcommand{\invocation}[1]{\par\vspace{.55\baselineskip}{\raggedright\itshape\leftskip=1em\parindent=-1em #1\par}}
\newcommand{\conclusion}[1]{\par\vspace{.55\baselineskip}{\noindent\itshape #1\par}}
\RequirePackage{needspace}
\newcommand{\acte}[2][]{\par\ifbib@apres\vspace{3mm plus 2mm}\fi\global\bib@aprestrue\needspace{7\baselineskip}\ifx\relax#1\relax\section{#2}\else\section[#1]{#2}\fi}
%% Indulgences : en tout petit, sous la priere
\newcommand{\indulg}[1]{\par\vspace{.3\baselineskip}{\raggedright\noindent\fontsize{6.4}{7.6}\selectfont\color{encre!80}\textsc{Ind.}\enspace\itshape #1\par}\vspace{.1\baselineskip}}
%% Hymne : latin a gauche, traduction a droite
\newcommand{\strophe}[2]{\par\vspace{.35\baselineskip}\noindent\begin{minipage}[t]{.47\linewidth}\raggedright\itshape #1\end{minipage}\hfill\begin{minipage}[t]{.49\linewidth}\raggedright\fontsize{8.2}{10}\selectfont #2\end{minipage}\par\vspace{.25\baselineskip}}
\newenvironment{litanie}{\par\vspace{.3\baselineskip}\begingroup\raggedright\fontsize{8.8}{10.6}\selectfont\leftskip=1em\parindent=-1em\parskip=.6pt\def\item{\par}}{\par\endgroup}
\newcommand{\fiche}[3]{\par\vspace{.6mm}{\raggedright\noindent\hangindent=1em{\color{rubrique}\petitescaps #1}\enspace #2.\enspace{\fontsize{7.4}{9}\selectfont\itshape #3}\par}}
\newcommand{\strophew}[2]{\par\vspace{.35\baselineskip}\noindent\begin{minipage}[t]{.585\linewidth}\raggedright\fontsize{8.4}{10.2}\selectfont\itshape\leftskip=.8em\parindent=-.8em #1\end{minipage}\hfill\begin{minipage}[t]{.39\linewidth}\raggedright\fontsize{8}{9.7}\selectfont #2\end{minipage}\par\vspace{.25\baselineskip}}
\newcommand{\usage}[1]{\par\vspace{-1mm}{\raggedright\noindent\fontsize{6.8}{8.2}\selectfont{\color{rubrique}usage :}\enspace\itshape #1\par}\nopagebreak[4]\vspace{1.2mm}\nopagebreak[4]}
\newcommand{\jour}[1]{\par\vspace{4mm}\needspace{10\baselineskip}{\centering\color{rubrique}\rule[.6ex]{10mm}{.3pt}\enspace{\fontsize{11.5}{14}\selectfont\scshape #1}\enspace\rule[.6ex]{10mm}{.3pt}\par}\vspace{1mm}\global\bib@apresfalse}
\newcommand{\sousacte}[1]{\par\vspace{2mm}\needspace{5\baselineskip}{\noindent\fontsize{10}{12}\selectfont\titrefont\scshape\color{rubrique}#1\par}\nopagebreak[4]\vspace{1mm}\nopagebreak[4]}
%% Elements liturgiques : le rouge devient fonctionnel (rubriques)
\newcommand{\rubrique}[1]{\par\vspace{.3\baselineskip}{\noindent\fontsize{8.4}{10.2}\selectfont\itshape\color{rubrique}#1\par}\nopagebreak[4]\vspace{.15\baselineskip}\nopagebreak[4]}
\newcommand{\intertitre}[1]{\par\vspace{.6\baselineskip}\nopagebreak[4]{\noindent\petitescaps\fontsize{8.8}{10.6}\selectfont\addfontfeature{LetterSpace=6}\color{rubrique}#1\par}\nopagebreak[4]\vspace{.25\baselineskip}\nopagebreak[4]}
\newcommand{\V}{{\color{rubrique}\ebgsymb ℣.}\ }
\newcommand{\R}{{\color{rubrique}\ebgsymb ℟.}\ }
\newcommand{\vr}[2]{\par{\noindent\V#1\par}{\noindent\R#2\par}}
\newcommand{\latin}[1]{\textit{#1}}
\newcommand{\traduction}[1]{\par{\noindent\fontsize{8.4}{10.2}\selectfont[#1]\par}}
\newenvironment{notice}{\par\vspace{.3\baselineskip}\fontsize{8.2}{10}\selectfont}{\par\vspace{.3\baselineskip}}
\newcommand{\source}[1]{\par{\raggedleft\fontsize{7.6}{9.2}\selectfont\itshape #1\par}}
\newcommand{\priere}{\par\noindent}
%% mysteres : numero rouge, intitule, fruit en italique
\newcommand{\mystere}[3]{\par\vspace{.12\baselineskip}{\noindent{\color{rubrique}\petitescaps #1}\enspace #2\par}{\leftskip=1.1em\noindent\fontsize{8.6}{10.4}\selectfont\textit{\fruitlabel} #3\par}}
\newcommand{\fruitlabel}{Fruit :}
\newcommand{\salut}[2]{\par\vspace{.25\baselineskip}{\noindent{\color{rubrique}\chiffresalignes #1.}\enspace #2\par}}
%% Une priere de deux pages s'ouvre sur une page paire : elle se lit d'un seul regard, sans tourner
\newcommand{\versgauche}{\clearpage\ifodd\value{page}\null\thispagestyle{empty}\clearpage\fi}
\newcommand{\versdroite}{\clearpage\ifodd\value{page}\else\null\thispagestyle{empty}\clearpage\fi}
\newcommand{\acteverso}[1]{\acte{#1}}
\newcommand{\acterecto}[1]{\acte{#1}}

%% 9. TABLE
\RequirePackage{titletoc}
\titlecontents{chapter}[0pt]{\addvspace{4mm}\petitescaps\color{rubrique}}{}{}{\hfill}
\titlecontents{section}[3mm]{\addvspace{1.2mm}\rightskip=7mm plus 1fil\parfillskip=-\rightskip\hyphenpenalty=10000}{}{}{\titlerule*[.6pc]{\scalebox{.5}{.}}\contentspage}
\renewcommand{\contentsname}{Table}

%% 10. PAGES LIMINAIRES ET COLOPHON
\newcommand{\bib@titre}{}     \renewcommand{\title}[1]{\renewcommand{\bib@titre}{#1}}
\newcommand{\bib@soustitre}{} \newcommand{\soustitre}[1]{\renewcommand{\bib@soustitre}{#1}}
\newcommand{\faussetitre}{\thispagestyle{empty}\null\vspace*{30mm}\par
  {\raggedright\petitescaps\fontsize{10.5}{13}\selectfont\addfontfeature{LetterSpace=14}\bib@titre\par}
  \vspace{9mm}\fleuronpetit\clearpage}
\newcommand{\pagedetitre}{\thispagestyle{empty}\cadre\begingroup\raggedright\null\vspace*{14mm}\par
  \filetdouble\vspace{7mm}
  {\fontsize{19}{23}\selectfont\titrefont\scshape\color{rubrique}\bib@titre\par}
  \ifx\bib@soustitre\empty\else\vspace{4mm}{\fontsize{10.5}{13.5}\selectfont\itshape\bib@soustitre\par}\fi
  \vspace{7mm}\filetdouble\vfill\noindent\monogramme\par\vspace*{8mm}\endgroup\clearpage}
\newcommand{\colophon}[1]{\clearpage\thispagestyle{empty}\null\vspace*{\fill}
  \begingroup\raggedright\fleuronpetit\vspace{4mm}
  {\fontsize{8.6}{12}\selectfont\itshape #1\par}\endgroup\vspace*{12mm}}
\endinput
