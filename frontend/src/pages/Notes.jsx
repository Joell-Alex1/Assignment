import React, { useState, useEffect } from "react";
import axios from "axios";

const Notes = () => {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [search, setSearch] = useState("");
  const [editingId, setEditingId] = useState(null);

  const token = localStorage.getItem("token");
  const config = { headers: { Authorization: `Bearer ${token}` } };

  const fetchNotes = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/notes", config);
      setNotes(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await axios.put(
          `http://127.0.0.1:8000/notes/${editingId}`,
          { title, content },
          config
        );
        setEditingId(null);
      } else {
        await axios.post(
          "http://127.0.0.1:8000/notes",
          { title, content },
          config
        );
      }
      setTitle("");
      setContent("");
      fetchNotes();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/notes/${id}`, config);
      fetchNotes();
    } catch (err) {
      console.error(err);
    }
  };

  const handleEdit = (note) => {
    setEditingId(note.id);
    setTitle(note.title);
    setContent(note.content);
  };

  const filteredNotes = notes.filter(
    (note) =>
      note.title.toLowerCase().includes(search.toLowerCase()) ||
      note.content.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-center text-blue-700">
        Notes Dashboard
      </h1>

      {/* Search */}
      <input
        type="text"
        placeholder="Search notes..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="border rounded-lg p-3 w-full mb-6 focus:outline-none focus:ring-2 focus:ring-blue-400"
      />

      {/* Note form */}
      <form onSubmit={handleSubmit} className="mb-8 bg-gray-50 p-4 rounded-lg shadow">
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="border rounded-md p-2 w-full mb-3 focus:outline-none focus:ring-2 focus:ring-blue-300"
          required
        />
        <textarea
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="border rounded-md p-2 w-full mb-3 focus:outline-none focus:ring-2 focus:ring-blue-300"
          required
        />
        <button
          type="submit"
          className={`w-full py-2 rounded text-white font-semibold ${
            editingId ? "bg-yellow-500 hover:bg-yellow-600" : "bg-blue-500 hover:bg-blue-600"
          }`}
        >
          {editingId ? "Update Note" : "Add Note"}
        </button>
      </form>

      {/* Notes list */}
      <div className="grid md:grid-cols-2 gap-4">
        {filteredNotes.map((note) => (
          <div
            key={note.id}
            className="bg-white p-4 rounded-lg shadow flex flex-col justify-between"
          >
            <div>
              <h2 className="font-bold text-lg mb-2">{note.title}</h2>
              <p className="text-gray-700">{note.content}</p>
            </div>
            <div className="mt-3 flex gap-2">
              <button
                onClick={() => handleEdit(note)}
                className="flex-1 bg-yellow-400 text-white rounded-md py-1 hover:bg-yellow-500"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(note.id)}
                className="flex-1 bg-red-500 text-white rounded-md py-1 hover:bg-red-600"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Notes;
