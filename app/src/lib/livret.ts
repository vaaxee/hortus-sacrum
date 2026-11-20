/**
 * Pièces du livret (data/prieres/jardin.json) → textes de l'app. Module pur (sans base), utilisable dans les scripts
 * Node et les tests.
 */
import type { Texte } from './types.ts';
import { SOURCE_VIDE } from './types.ts';

/** Conversion des pièces du livret (data/prieres/jardin.json) vers le balisage de l'app. */

interface Bloc {
	type: string;
	texte?: string;
	v?: string;
	r?: string;
	la?: string;
	fr?: string;
	items?: string[];
	numero?: string;
	fruit?: string;
	fruit_libelle?: string;
	titre?: string;
	note?: string;
}

export interface Piece {
	id: string;
	ordre: number;
	titre: string;
	type: string;
	partie: { numero: string; titre: string } | null;
	jour_de_semaine: string | null;
	page_livret: number | null;
	usage: string | null;
	indulgence: string | null;
	source: string | null;
	blocs: Bloc[];
}

export function blocsVersCorps(blocs: Bloc[]): { corps: string; latin: string } {
	const fr: string[] = [];
	const la: string[] = [];
	for (const b of blocs) {
		switch (b.type) {
			case 'texte':
			case 'conclusion':
				fr.push(b.type === 'conclusion' ? `*${b.texte}*` : (b.texte ?? ''));
				break;
			case 'rubrique':
			case 'notice':
				fr.push(`[r]${(b.texte ?? '').replace(/\n+/g, ' ')}[/r]`);
				break;
			case 'intertitre':
				fr.push(`## ${b.texte}`);
				break;
			case 'traduction':
				fr.push(`[${b.texte}]`);
				break;
			case 'invocation':
				fr.push(b.texte ?? '');
				break;
			case 'verset':
				fr.push(`℣. ${b.v}\n℟. ${b.r}`);
				break;
			case 'strophe':
				fr.push(b.fr ?? '');
				la.push(b.la ?? '');
				break;
			case 'litanie':
				fr.push((b.items ?? []).join('\n'));
				break;
			case 'mystere':
				fr.push(`[r]${b.numero}[/r] ${b.texte}\n*${b.fruit_libelle}* ${b.fruit}`);
				break;
			case 'numero':
				fr.push(`[r]${b.numero}.[/r] ${b.texte}`);
				break;
			case 'fiche':
				fr.push(`[r]${b.titre}[/r] ${b.texte}. *${b.note}*`);
				break;
			default:
				if (b.texte) fr.push(b.texte);
		}
	}
	return { corps: fr.filter(Boolean).join('\n\n'), latin: la.filter(Boolean).join('\n\n') };
}

export function pieceVersTexte(p: Piece): Texte {
	const { corps, latin } = blocsVersCorps(p.blocs);
	const t: Texte = {
		id: `jardin:${p.id}`,
		origine: 'livret',
		titre: p.titre,
		partie: p.partie ? p.partie.titre : '',
		categorie: p.jour_de_semaine ?? '',
		corps,
		latin,
		usage: p.usage ?? '',
		indulgence: p.indulgence ?? '',
		source: {
			...SOURCE_VIDE,
			ouvrage: p.source ?? '',
			edition: 'Le Jardin de l’âme (livret)',
			page: p.page_livret ? String(p.page_livret) : ''
		},
		ordre: p.ordre,
		creeLe: '',
		modifieLe: ''
	};
	return t;
}
