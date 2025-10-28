type Props = {
  params: Promise<{ id: string }>;
};

export default async function NoteDetailPage({ params }: Props) {
  const { id } = await params;

  return (
    <main className="mx-auto max-w-3xl p-6 space-y-3">
      <h1 className="text-2xl font-semibold">Note #{id}</h1>
      <p className="text-sm text-gray-600">
        Details view placeholder for testing/dev purposes, we'll wire this to the backend later.
      </p>
    </main>
  );
}