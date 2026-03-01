// Fetch all students and display in table
async function fetchStudents() {
    const response = await fetch("/students/");   // IMPORTANT: trailing slash
    const data = await response.json();

    const tableBody = document.querySelector("#studentTable tbody");
    tableBody.innerHTML = "";

    data.forEach(student => {
        const row = `
            <tr>
                <td>${student.student_id}</td>
                <td>${student.name}</td>
                <td>${student.age}</td>
                <td>${student.course}</td>
                <td>${student.marks}</td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}

// Add new student
async function addStudent() {
    const student_id = document.getElementById("student_id").value;
    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;
    const course = document.getElementById("course").value;
    const marks = document.getElementById("marks").value;

    if (!student_id || !name || !age || !course || !marks) {
        alert("Please fill all fields");
        return;
    }

    const response = await fetch("/students/", {   // IMPORTANT: trailing slash
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            student_id: parseInt(student_id),
            name: name,
            age: parseInt(age),
            course: course,
            marks: parseInt(marks)
        })
    });

    const result = await response.json();
    console.log(result);

    // Clear form
    document.getElementById("student_id").value = "";
    document.getElementById("name").value = "";
    document.getElementById("age").value = "";
    document.getElementById("course").value = "";
    document.getElementById("marks").value = "";

    fetchStudents();
}

// Load students when page opens
fetchStudents();