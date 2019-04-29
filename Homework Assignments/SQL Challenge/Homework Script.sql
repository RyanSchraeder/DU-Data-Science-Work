SET SQL_SAFE_UPDATES = 0;

-- Select the first & last name of all actors/actresses
SELECT * FROM sakila.actor;
SELECT first_name, last_name FROM sakila.actor;

-- Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
SELECT CONCAT (UPPER(first_name), ' ', UPPER(last_name))
AS 'Actor Name'
FROM sakila.actor;

-- 2a. You need to find the ID number, first name, and last name of an actor,
-- of whom you know only the first name, "Joe." What is one query would you 
-- use to obtain this information?

SELECT  actor_id, first_name, last_name 
  FROM ACTOR
 WHERE first_name = 'Joe'
;

-- Find all actors whose last name contain the letters GEN:
SELECT first_name, last_name 
	FROM ACTOR
WHERE last_name like '%GEN%'; 

-- Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
SELECT last_name, first_name
	FROM ACTOR
WHERE last_name like '%LI%'; 

-- Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
SELECT country_id, country FROM country
WHERE country IN ('Afghanistan', 'Bangladesh', 'China');

-- 3a. Add a `middle_name` column to the table `actor`. Position it between 
-- `first_name` and `last_name`. Hint: you will need to specify the data type
ALTER TABLE actor ADD middle_name VARCHAR( 255 ) AFTER first_name;

-- 3b. You realize that some of these actors have tremendously long last 
-- names. Change the data type of the `middle_name` column to `blobs`.
ALTER TABLE ACTOR MODIFY middle_name BLOB;

-- 3c. Now delete the `middle_name` column.
DELETE middle_name FROM actor; 

-- 4a. List the last names of actors, as well as how many actors have that
-- last name
SELECT last_name, count(*) last_name 
FROM actor 
GROUP BY  actor.last_name
;

-- 4b List last names of actors and the number of actors who have that last
--    name, but only for names that are shared by at least two actors
SELECT last_name
	, count(*) last_name 
FROM actor
GROUP BY actor.last_name
HAVING count(*) >= 2
;
-- 4c. Oh, no! The actor `HARPO WILLIAMS` was accidentally entered in the 
--     `actor` table as `GROUCHO WILLIAMS`, the name of Harpo's second 
--     cousin's husband's yoga teacher. Write a query to fix the record.

SELECT * FROM ACTOR 
 WHERE first_name  = 'GROUCHO' 
 AND last_name = 'WILLIAMS'
;
UPDATE ACTOR 
   SET first_name = 'HARPO' 
 WHERE first_name  = 'GROUCHO' 
 AND last_name = 'WILLIAMS'
;
SELECT * FROM ACTOR 
 WHERE first_name  = 'HARPO'
 AND last_name = 'WILLIAMS'
;

/*4d. Perhaps we were too hasty in changing `GROUCHO` to `HARPO`. 
It turns out that `GROUCHO` was the correct name after all! In a single 
query, if the first name of the actor is currently `HARPO`, change it to 
`GROUCHO`. Otherwise, change the first name to `MUCHO GROUCHO`, as that is
 exactly what the actor will be with the grievous error. BE CAREFUL NOT TO
 CHANGE THE FIRST NAME OF EVERY ACTOR TO `MUCHO GROUCHO`, HOWEVER! 
 (Hint: update the record using a unique identifier.)
*/
SELECT * FROM actor
WHERE actor_id = 172
;
UPDATE ACTOR SET first_name = 
  CASE WHEN first_name = 'HARPO'
         THEN 'GROUCHO'
		 ELSE 'MUCHO GROUCHO'
  END
 WHERE ACTOR_ID  = 172
;
-- 5a. . You cannot locate the schema of the `address` table. Which query 
-- would you use to re-create it?
-- Hint: <https://dev.mysql.com/doc/refman/5.7/en/show-create-table.html>

SHOW CREATE TABLE address;

-- Copied table query for later use
-- CREATE TABLE `address` (
--   `address_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
--   `address` varchar(50) NOT NULL,
--   `address2` varchar(50) DEFAULT NULL,
--   `district` varchar(20) NOT NULL,
--   `city_id` smallint(5) unsigned NOT NULL,
--   `postal_code` varchar(10) DEFAULT NULL,
--   `phone` varchar(20) NOT NULL,
-- `location` geometry NOT NULL,
--   `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
--  PRIMARY KEY (`address_id`),
--   KEY `idx_fk_city_id` (`city_id`),
-- SPATIAL KEY `idx_location` (`location`),
--   CONSTRAINT `fk_address_city` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`) ON UPDATE CASCADE
-- ) ENGINE=InnoDB AUTO_INCREMENT=606 DEFAULT CHARSET=utf8
 
/*6a. Use `JOIN` to display the first and last names, as well as the address,
  of each staff member. Use the tables `staff` and `address`:*/

SELECT S.first_name, S.last_name, address.address
FROM staff S
LEFT JOIN address ON S.address_id = address.address_id; 


 /*6b. Use `JOIN` to display the total amount rung up by each staff member in August of 2005. 
Use tables `staff` and `payment`.*/


SELECT P.staff_id, P.payment_date
	,concat(S.first_name,' ',S.last_name) AS Name
	,SUM(P.amount) as 'Total Amount'
FROM payment P, staff S
WHERE MONTH (P.payment_date) = 08 
  AND YEAR(P.payment_date) = 2005
  AND P.staff_id = S.staff_id 
GROUP BY P.staff_id
;

/*6c. List each film and the number of actors who are listed for that film. 
Use tables `film_actor` and `film`. Use inner join. */

SELECT film.title, COUNT(film_actor.actor_id) AS 'Actor Count'
		FROM film_actor, film
        WHERE film_actor.film_id = film.film_id
		GROUP BY film_actor.film_id
	;

/*6d. How many copies of the film `Hunchback Impossible` exist in the inventory system? */

SELECT inventory.film_id, film.title, count(inventory.inventory_id) AS 'Copies'
-- join by selecting columns from both tables inventory, film
FROM inventory, film
WHERE inventory.film_id IN
-- create subquery for Hunchback Impossible
		(SELECT film.film_id FROM film
			WHERE film.title LIKE 'Hunchback Impossible')
	AND inventory.film_id = film.film_id
GROUP BY 1
;
 
/*6e. Using the tables `payment` and `customer` and the `JOIN` command, 
list the total paid by each customer. List the customers alphabetically by last name: */

SELECT customer.first_name AS 'First Name', 
       customer.last_name AS 'Last Name',
       SUM(payment.amount) AS Total
	FROM payment, customer
    WHERE payment.payment_id = customer.customer_id
GROUP BY customer.last_name, customer.first_name
ORDER BY customer.last_name
;

/* 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. 
As an unintended consequence, films starting with the letters `K` and `Q` have 
also soared in popularity. Use subqueries to display the titles of movies starting 
with the letters `K` and `Q` whose language is English.*/

 -- SELECT DISTINCTROW 'English' FROM language;
SELECT F.title 
	FROM film F
	WHERE (F.title LIKE 'K%') OR (F.title LIKE 'Q%') 
      AND F.language_id = 
		(SELECT language_id FROM language
			WHERE name = 'English')
;

-- SELECT * FROM language;
-- Keeps returning only title, revisit 

-- 7b. Use subqueries to display all actors who appear in the film `Alone Trip`.
--     Film id is 17 for 'Alone Trip'

SELECT 
	CONCAT(actor.first_name, ' ', actor.last_name) AS 'Actor Name'
    FROM film_actor, actor
	WHERE film_actor.actor_id = actor.actor_id
	  AND film_actor.film_id =
		(SELECT film.film_id 
		   FROM film
		   WHERE film.title = 'Alone Trip')
;
	
 -- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and 
 -- email addresses of all Canadian customers. Use joins to retrieve this information.
 
SELECT CONCAT(C.first_name, ' ', C.last_name) AS 'Customer Name'
		,C.address_id
FROM customer C
WHERE C.address_id IN (
		SELECT A.address_id
		FROM address A, city C, country CO
		WHERE CO.country= 'Canada'
		  AND CO.country_id = C.country_id
		  AND A.city_id = C.city_id  
		)
;

-- 7d.
-- Sales have been lagging among young families, and you wish to target all family movies 
-- for a promotion. Identify all movies categorized as family films.

SELECT category.name, film.title
	FROM film, category
	WHERE (category.name = 'Family')
;

/* 7e. Display the most frequently rented movies in descending order. */

SELECT inventory.film_id, film.title, count(*) as 'Rent Count'
FROM rental, film, inventory
WHERE rental.inventory_id = inventory.inventory_id
AND inventory.film_id = film.film_id
GROUP BY inventory.film_id, film.title
ORDER BY 'Rent Count' DESC;

/* 7f. Write a query to display how much business, in dollars, each store brought in. 
Use  PAYMENT, CUSTOMER */

SELECT customer.store_id, SUM(payment.amount) as 'Revenue'
    FROM payment, customer
	WHERE payment.customer_id = customer.customer_id
	GROUP BY customer.store_id
;

/* 7g. Write a query to display for each store its store ID, city, and country.*/
		-- Use Store, address, city country

SELECT store.store_id, address.address, country.country, address.city_id
FROM store, address, country
WHERE store.address_id  = address.address_id
;
/* 7h. List the top five genres in gross revenue in descending order. (**Hint**: you may need to 
use the following tables: category, film_category, inventory, payment, and rental.)*/
SELECT category.name AS Genre, SUM(payment.amount) as 'GROSS REVENUE'
  FROM   category
		,film_category   
        ,inventory 
        ,payment
        ,rental
WHERE 	payment.rental_id = rental.rental_id
  AND   rental.inventory_id = inventory.inventory_id
  AND   inventory.film_id = film_category.film_id
  AND   film_category.category_id = category.category_id
GROUP BY Genre
ORDER BY 2 DESC
LIMIT 5 
;  

/* 8a. In your new role as an executive, you would like to have an easy way of viewing 
the Top five genres by gross revenue. Use the solution from the problem above to create a view. 
If you haven't solved 7h, you can substitute another query to create a view.*/

CREATE VIEW Genre_Revenue_Breakdown AS 
	(SELECT category.name AS Genre, SUM(payment.amount) as 'GROSS REVENUE'
		FROM category
			,film_category   
			,inventory 
			,payment
			,rental
		WHERE 	payment.rental_id = rental.rental_id
		AND   rental.inventory_id = inventory.inventory_id
		AND   inventory.film_id = film_category.film_id
		AND   film_category.category_id = category.category_id
GROUP BY Genre
ORDER BY 2 DESC
LIMIT 5)
;  

/* 8b. How would you display the view that you created in 8a?*/ 
		-- Use below query to display all rows from the view. 

SHOW CREATE VIEW Genre_Revenue_Breakdown;
SELECT * FROM Genre_Revenue_Breakdown;

-- 8c. You find that you no longer need the view `top_five_genres`. Write a query 
-- to delete it.
DROP VIEW IF EXISTS Genre_Revenue_Breakdown; 
