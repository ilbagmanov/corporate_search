package ru.itits.diploma.corporate_search.dto;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.itits.diploma.corporate_search.model.Document;

@Repository
public interface DocumentRepository extends JpaRepository<Document, Long> {
}
