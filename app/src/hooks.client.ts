/** Le message réel d'une erreur inattendue (et non « Internal Error »), affiché par la page d'erreur. */
export const handleError = ({ error, message }: { error: unknown; message: string }) => {
	const e = error instanceof Error ? error : null;
	console.error(error);
	return { message: e ? `${e.name} : ${e.message}` : message };
};
