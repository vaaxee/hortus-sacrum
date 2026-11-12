import { describe, expect, it } from 'vitest';
import { assembler, decouper } from './importer.ts';

describe('decouper', () => {
	const texte = assembler([
		{ page: 12, texte: 'Premier titre\n\nTexte de la première pièce, page douze.', ocr: false },
		{ page: 13, texte: 'Suite de la première pièce.\n\n=== Deuxième pièce\nTexte de la deuxième.', ocr: false },
		{ page: 14, texte: 'Fin de la deuxième.', ocr: true }
	]);

	it('une seule pièce sans marque, avec ses pages', () => {
		const p = decouper('⟦p. 5⟧\nTitre court\n\nCorps du texte.\n\n⟦p. 6⟧\nSuite.');
		expect(p).toHaveLength(1);
		expect(p[0]).toEqual({ titre: 'Titre court', corps: 'Corps du texte.\n\nSuite.', pages: '5-6' });
	});

	it('coupe aux lignes === et suit les pages', () => {
		const p = decouper(texte);
		expect(p.map((x) => x.titre)).toEqual(['Premier titre', 'Deuxième pièce']);
		expect(p.map((x) => x.pages)).toEqual(['12-13', '13-14']);
		expect(p[1].corps).toBe('Texte de la deuxième.\n\nFin de la deuxième.');
		expect(p[0].corps).not.toContain('⟦');
	});

	it('titre par défaut numéroté quand rien ne l’indique', () => {
		const p = decouper('Un seul long paragraphe sans titre.\n=== \nAutre paragraphe.', 'Recueil');
		expect(p.map((x) => x.titre)).toEqual(['Recueil (1)', 'Recueil (2)']);
	});
});
