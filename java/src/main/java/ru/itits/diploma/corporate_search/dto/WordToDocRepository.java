package ru.itits.diploma.corporate_search.dto;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.itits.diploma.corporate_search.model.WordToDoc;

@Repository
public interface WordToDocRepository extends JpaRepository<WordToDoc, Long> {
}
