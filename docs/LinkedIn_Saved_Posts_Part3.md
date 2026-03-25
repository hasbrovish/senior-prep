LINKEDIN SAVED POSTS \- PART 3 (Posts 301-447)  
\==============================================

\=== POST 301 \===  
Status is reachable  
David Heinemeier Hansson  
View David Heinemeier Hansson’s profile  
   
• 1st  
Co-owner & CTO of 37signals (Makers of Basecamp \+ HEY)

3yr •   
3yr Visible to everyone

Disappointment occurs when expectations don’t match reality. And our expectations for software quality are profoundly unrealistic. Thus, lots of people are continuously disappointed — even enraged — by software bugs. They shouldn’t be.

The only reliable, widely used way to ensure impeccable software quality is to write less software that does less stuff, and then spend eons honing that tiny lot. Such an approach, however, is very rarely compatible with commercial success or even programmer motivations (despite what many may claim).

Bugs are an inevitable byproduct of writing software. Sure, there are all sorts of techniques and potions that promise to decrease how many of the damn critters run about, but only the comically hyperbole pretends that complete eradication is possible.

Once we accept that simple fact that software \= bugs, we can progress to understand why fixing them may not even be that important a lot of the time. The absence of bugs is simply one parameter of success in software, but not even close to the most important one (with some exception for life critical systems).

Useless software can be entirely bug free, yet remain entirely useless. Useful software can be ridden with bugs, yet remain highly valuable. Or, the value of software depends far more upon the problem it solves than the quality by which it does so.

The value of a any given bug can be rated by the number of users affected times the criticality of the issue. Lots of users are losing all their data due to this bug? Okay, then, Very Damn Important\! Fix it NOW\! Lots of users are a little annoyed or confused by this? Probably should fix it some time soon. A few users have to spend another 30 seconds on a work around? Unlikely to get fixed any time soon\!

Software organizations that stay in business triage their backlog of bugs like that. They do not drop everything to deal with any damn bug. As the economies of scale kick in, so does the magnitude of consequences from such triaging. Large software packages and organizations will have hundreds if not thousands if not TENS OF THOUSANDS of open bugs of various criticality. THIS IS NORMAL. THIS IS EXPECTED.

This is not a call to give up on software quality, quite the contrary. This is a call to remove the highly-charged emotional responses of encountering the world as it should be expected to spin. Demeaning developers, questioning their professionalism (whatever that means\!), or feigning outrage at that which ails all software makes everyone, including users, worse off.

So next time you hit an annoying bug, give it five minutes before you fire off that indignant tweet. Marvel at the miracle it is that anything as complex as a modern piece of software works at all\! Consider the billions of instructions our work-horse CPUs have to get just right for you to enjoy the splendors of computing. Have some sympathy for man and machine.

https://lnkd.in/epFE7MAK  
…see more

Software has bugs. This is normal.

world.hey.com

\=== POST 302 \===  
Abhishek Somani  
View Abhishek Somani’s profile  
   
• 2nd  
Engineer at Coinbase | Ex-Amazon | Ex-Microsoft

3yr •   
3yr Visible to everyone

I have been enjoying coding in Go since I joined Coinbase.   
Really excited to see the Go team release version 𝟭.𝟮𝟬 a few days ago. It includes a handful of language changes, many improvements to tooling and the library, and better overall performance. Here are few highlights:

𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲 𝗰𝗵𝗮𝗻𝗴𝗲𝘀  
🚀 The predeclared comparable constraint is now also satisfied by ordinary comparable types, such as interfaces, which will simplify generic code.  
🚀 The functions SliceData, String, and StringData have been added to package unsafe. They complete the set of functions for implementation-independent slice and string manipulation.  
🚀 Go’s type conversion rules have been extended to permit direct conversion from a slice to an array.  
🚀 The language specification now defines the exact order in which array elements and struct fields are compared. This clarifies what happens in case of panics during comparisons.

𝗦𝘁𝗮𝗻𝗱𝗮𝗿𝗱 𝗹𝗶𝗯𝗿𝗮𝗿𝘆 𝗮𝗱𝗱𝗶𝘁𝗶𝗼𝗻𝘀  
🚀 The new crypto/ecdh package provides explicit support for Elliptic Curve Diffie-Hellman key exchanges over NIST curves and Curve25519.  
🚀 The new function errors.Join returns an error wrapping a list of errors which may be obtained again if the error type implements the Unwrap() \[\]error method.  
🚀 The new http.ResponseController type provides access to extended per-request functionality not handled by the http.ResponseWriter interface.  
🚀 The httputil.ReverseProxy forwarding proxy includes a new Rewrite hook function, superseding the previous Director hook.  
🚀 The new context.WithCancelCause function provides a way to cancel a context with a given error. That error can be retrieved by calling the new context.Cause function.  
🚀 The new os/exec.Cmd fields Cancel and WaitDelay specify the behavior of the Cmd when its associated Context is canceled or its process exits.

𝗜𝗺𝗽𝗿𝗼𝘃𝗲𝗱 𝗽𝗲𝗿𝗳𝗼𝗿𝗺𝗮𝗻𝗰𝗲  
🚀 Compiler and garbage collector improvements have reduced memory overhead and improved overall CPU performance by up to 2%.  
🚀 Work specifically targeting compilation times led to build improvements by up to 10%. This brings build speeds back in line with Go 1.17.

For more details about the release notes, please refer my comment on this post.

\#release \#go \#golang \#coding 

…see more

\=== POST 303 \===  
Milan Jovanović  
View Milan Jovanović’s profile  
   
• 2nd  
Practical .NET and Software Architecture Tips | Microsoft MVP

3yr •   
3yr Visible to everyone

I implemented completely decoupled communication between services using a queue.

Here's how I did it. 👇

Do you know what RPC is?

RPC (Remote Procedure Call) is a protocol for making a request from a client to a server and receiving a response.

One way to implement RPC calls using a queue is to use a message queue as an intermediary between the client and the server.

In my case, the client and the server are two backend services.  
But nothing changes conceptually.

Here's a general outline of the process:  
• Client sends a request message  
• Server processes request message  
• Server sends a response message  
• Client receives the response message

The client sends a request message to the message queue, containing all the necessary parameters for the desired operation. Usually, the request message is an interface that both services are aware of.

The server constantly listens to the queue, picks up the request message, and processes it.  
Processing can be performing an operation or returning some data.

The server then sends the response back to the client by sending a message to a response queue that the client listens to. It's important that the client and server expect the same interface for the response message.

The client receives the response message from the response queue and processes it.

Using a message queue, the client and server can communicate asynchronously, without establishing a direct connection.

This is great for decoupling your services and enables them to scale independently as the system grows.

If you enjoyed this post, then you will love my weekly .NET newsletter. Every Saturday I share one actionable .NET tip.

Join 8500+ engineers: https://lnkd.in/dMDPXuUh  
…see more

\=== POST 304 \===  
Manu Agrawal  
View Manu Agrawal’s profile  
   
• 2nd  
Senior Software Engineer | Agentic AI & Gen-AI | Full Stack Engineer | Joshtalks Speaker | Featured on 10+ News channels | Ex Google

3yr •   
3yr Visible to everyone

Best way to learn low level design

Github , LLD Primer  
https://lnkd.in/dtEY-4Av

Youtube Playlist by Shrayansh Jain   
https://lnkd.in/dhigHViK

Design Patterns Playlist  
https://lnkd.in/d36y4\_pz

Best Github Article   
https://lnkd.in/dfNiqcBx

Learn Language wise design Patterns  
https://lnkd.in/dT86MKHE

Do follow Manu Agrawal 

 \#github \#design \#language  
…see more

\=== POST 305 \===  
Denis Magda  
View Denis Magda’s profile  
   
• 2nd  
Platform Engineering & Developer Relations. Author of the “Just Use Postgres\!” book.

3yr •   
3yr Visible to everyone

How does Java litter beyond the heap? This question gave birth to a series of articles about garbage collection beyond the Java premises.

Take one of your Java applications. The app executes your logic in runtime, generating garbage in the heap. Then, the garbage collector steps in and dutifully removes dead objects. This is a known fact.

At the same time, this Java app might not live in isolation but communicates with services, databases, and other components. Some of those components also generate and collect garbage, while fulfilling the Java app's requests. This is less known.

For instance, garbage collection is used in relational databases such as PostgreSQL, distributed databases such as YugabyteDB, and in solid-state drives (yes, even hardware uses GC\!)

Want to learn more? 

First, start with the series of articles. Don't just read, pull up your sleeves and follow the tutorials:  
https://lnkd.in/eh6Zr7Ji   
   
Then, come for an in-depth hands-on workshop in the following locations:  
\* Boston JUG, Feb 7th: https://lnkd.in/eczmY5sc  
\* Charlotte JUG, Feb 9th: https://lnkd.in/ezhhpbix  
\* Seattle JUG, Feb 21st: https://www.seajug.org/  
\* Boulder JUG, March 7th: https://lnkd.in/e5FPMk8d  
\* Denver JUG, March 8th: https://lnkd.in/euwKwbTf  
\* Philly JUG, May 17th: https://lnkd.in/eYACV3mM

CC Miya Longwe Orlando Valdez Nimret Singh Sandhu Matt Raible

\#java \#postgresql \#yugabytedb   
…see more

\=== POST 306 \===  
Lalit Kundu  
View Lalit Kundu’s profile  
   
• 1st  
Healthtech Entrepreneur | ex-Google Leader | Wharton MBA

3yr •   
3yr Visible to everyone

If you want to grow in your career as an engineer, building trust with your technical leadership and management is critical. Equally important is building trust with your peers (other managers, TLs) and people you lead.  
   
This is where I’ve found the trust triangle helpful. Trust is founded on three equally important drivers – authenticity, logic, and empathy. Lacking in any of these drivers will cause trust issues.

Authenticity – it means being yourself, being true to your intentions. Be your unique self to others. You don’t agree with a certain solution, it’s okay to let others know (kindly), instead of secretly being disgruntled. You can open aspects of your personality (that you’re comfortable with) instead of being a closed box at work.

Empathy – opposite of being selfish. Do you care about your own goals or also what matters to the other person? Foster an open communication about needs of others (in career, or their goals for their team/project etc.). Make others heard.

Logic – this one I think everyone’s well aware of. Leading with data, logical arguments (instead of intuition), being clear about your methodologies, proving your technically sound judgment. This comes slowly with collaboration. 

When I read about the trust triangle (https://lnkd.in/g3aScFFk), I evaluated a lot of my roles at work to see how much trust I have, and how I can build more. I had great engineering skills, I was analytical and logical. What I was lacking somewhat was empathy, and I started working on that.

Do you find this helpful?  
✅ Subscribe to my biweekly newsletter to receive tips on how to grow in your software engineering career (https://lnkd.in/guVvnEb5).  
 📣 Repost to your network to add value to others' feed.

…see more

\=== POST 307 \===  
Asim Khan  
View Asim Khan’s profile  
   
• 2nd  
Engineer @ServiceNow | Ex-SAP, TCS | 91K+ Followers | 🚀 Talent Referrer | 🌍 Traveller | 📞 Mentor & Career Guide

3yr •   
3yr Visible to everyone

🎁Amidst all the \#layoffs, 🚀ServiceNow is \#hiring   
🔥Apply now through the \#referral links below for positions in India👇🏻

🛍 Either choose path A or path B, DONT do both\~\~  
\--------------------------------------------------  
Path A:   
If you don't find a relevant role in this post:

↗ Find relevant Job ID \- https://lnkd.in/dKAzBg6g  
↗ Fill out this form \- https://lnkd.in/dzxY6dpY  
\--------------------------------------------------

Path B:  
🔓 Software Engineer \[0-2+ yrs\]:  
https://smrtr.io/cWQNY  
https://smrtr.io/cWQR7 \[2+ yrs\]  
https://smrtr.io/cWQR\_ \[2+ yrs\]  
https://smrtr.io/cSgBC \[2+ yrs\]  
https://smrtr.io/cWRmS \[2+ yrs\]

🔓 Senior Software Engineer \[4-8 yrs\]:  
https://smrtr.io/cWQLF  
https://smrtr.io/cWQQV  
https://smrtr.io/cWQRC \[6+ yrs\]  
https://smrtr.io/cWQTB \[6+ yrs\]  
https://smrtr.io/cWQTM \[6+ yrs\]  
https://smrtr.io/cWRmG \[Devops\]

🔓 Staff Software Engineer \[8+ yrs\]:  
https://smrtr.io/cWQPY  
https://smrtr.io/cWQQF  
https://smrtr.io/cWQTq  
https://smrtr.io/cWRnd \[13+ yrs\]

🔓 Manager, Software Engineering \[10+ yrs exp\]  
10+ years of experience with technologies relevant to SN and advanced coding skills  
https://smrtr.io/cYv\_q  
https://smrtr.io/cYv\_s  
https://smrtr.io/cYv\_v  
https://smrtr.io/cYv\_w  
https://smrtr.io/cYv\_x

🔓 Software QA Engineer \[0-2+ yrs\]:  
https://smrtr.io/cWRkM

🔓 Senior Software QA Engineer \[ 4+ yrs\]:  
https://smrtr.io/cWQSR  
https://smrtr.io/cWQV2

🔓 Staff Software QA Engineer \[ 8+ yrs\]:  
https://smrtr.io/cWQVw

🔓 Senior people partner  
https://smrtr.io/cWRq6 \[6+ yrs\]

🔓 Certification Security Engineer  
https://smrtr.io/cWRJ4 \[3+ yrs\]

🔓 Senior Product Designer  
https://smrtr.io/cWRMG \[5+ yrs\]

Please \#share this with anyone who has been \#laidoff and is looking for a \#jobchange 🤗 

\#designer \#security \#humanresource \#cybersecurity \#hr \#jobfinder \#jobalert \#careers \#sde2 \#sde3 \#softwareengineers   
\#jobsearch \#happytohelp \#layoff \#microsoft \#google \#amazon \#twitter \#salesforce \#techlayoffs \#hiring \#jobopening \#job \#joboppurtunity \#hiringnow \#jobcuts \#openings \#qa \#engineer \#softwareengineer \#devops \#productdesigner \#humanresourcesjobs \#freshersjobs \#freshers \#applynow \#helpinghands \#helpingpeople \#faang \#programming \#problemsolving \#dsa \#systemdesign \#people \#career \#engineering \#hiringpost \#hiringnow \#referral \#referralprogram \#h1b \#h1bjobs \#LinkedIn \#networking \#CareerAdvice \#Leadership \#Business \#Marketing \#Entrepreneurship \#Innovation \#Layoffs \#JobLoss \#Unemployment \#Hiring \#CareerTransition \#OpenToWork \#LookingForWork \#JobSearch \#Networking \#CareerOpportunities  
…see more

\=== POST 308 \===  
Aakash Kanojiya  
View Aakash Kanojiya’s profile  
   
• 2nd  
𝐀𝐈 𝐄𝐧𝐭𝐡𝐮𝐬𝐢𝐚𝐬𝐭 | 𝐅𝐮𝐥𝐥 𝐒𝐭𝐚𝐜𝐤 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 | 𝐆𝐫𝐨𝐰𝐭𝐡 𝐌𝐚𝐫𝐤𝐞𝐭𝐞𝐫 | 𝐒𝐡𝐚𝐫𝐢𝐧𝐠 𝐈𝐧𝐬𝐢𝐠𝐡𝐭𝐬 𝐨𝐧 𝐀𝐈 | 𝐓𝐞𝐜𝐡𝐧𝐢𝐜𝐚𝐥 𝐂𝐨𝐧𝐭𝐞𝐧𝐭 𝐖𝐫𝐢𝐭𝐞𝐫

3yr •   
3yr Visible to everyone

𝐑𝐞𝐚𝐥 𝐋𝐢𝐟𝐞 𝐀𝐩𝐩𝐥𝐢𝐜𝐚𝐭𝐢𝐨𝐧𝐬 𝐨𝐟 𝐃𝐚𝐭𝐚 𝐒𝐭𝐫𝐮𝐜𝐭𝐮𝐫𝐞𝐬 𝐮𝐬𝐞𝐝 𝐢𝐧 𝐨𝐮𝐫 𝐃𝐚𝐲 𝐭𝐨 𝐝𝐚𝐲 𝐥𝐢𝐟𝐞 \!\!\!

𝐒𝐡𝐚𝐫𝐞 𝐭𝐡𝐞 𝐩𝐨𝐬𝐭 𝐰𝐢𝐭𝐡 𝐲𝐨𝐮𝐫 𝐧𝐞𝐭𝐰𝐨𝐫𝐤 𝐢𝐟 𝐲𝐨𝐮 𝐟𝐢𝐧𝐝 𝐢𝐭 𝐮𝐬𝐞𝐟𝐮𝐥.

Add the examples or applications which you know in the comments section

Follow Aakash Kanojiya for more

\#programming \#coding \#technology \#tech \#datastructures \#dsa   
…see more

DSA

\=== POST 309 \===  
Devanshu .  
View Devanshu .’s profile  
   
• 1st  
Senior Software Engineer @ Coda Payments

3yr •   
3yr Visible to everyone

\#systemdesign problem I am working on right now at \#microsoft as a Mid-level engineer

Layman problem statement:   
\- We have a \#csharp service.   
\- Fetches data(pull model) from two input sources, combines them in complex ways and produces records of multiple types  
\- Corresponding to each record type, do special calculation and prepare standard record. There are around 10 different types.  
\- dump data into message queue and submit to downstream.

Team Context:   
Our teams does compute on \#azure stream analytics which is a stream processing engine.  
You write the computation logic in \#sql like language.  
We currently run 15K jobs in productions. Billions of records processed per day.  
Hehe, yes\!\! Insane scale.

Scope of my work in layman terms:  
I need to convert the whole service into a data pipeline comprised of multiple jobs connected by message queues in between.  
The computation logic which was in c\# needs to be converted into \#sql like queries.

Which means,  
\- Pull Model becomes Push model. You get the data in a stream and not fetched on demand when you want it.  
\- Data combination becomes join between 2 streams. That for loop you wrote earlier, well not anymore 🤣   
\- Note that the joins are not on static data but rather free flowing streaming data with time constriants.  
\- Your if statements becomes where clauses.  
\- In between you need to think about partitioning of the inputs because the input streams are huge.  
\- If you were querying past data, meaning not from current time window, it becomes insanely hard to model it in streaming world. Possible, but hard.

Have you worked on \#streamprocessing or \#batchprocessing systems? Comment you experience below.  
I can certainly get some insights.

\#softwaredevelopment \#softwareengineering \#dataprocessing \#technology   
…see more

\=== POST 310 \===  
Ben Meer  
View Ben Meer’s profile  
   
• 3rd+  
The Systems Guy • Follow me for systems on health, wealth, and free time ⚡ Cornell MBA • 2M+ audience

3yr •   
3yr Visible to everyone

The best method to learn anything, according to a Nobel Prize winner:

The Feynman Technique:

\=== POST 311 \===  
Neel Thomas  
View Neel Thomas’ profile  
   
• 2nd  
Sr. Software Engineer (AI Ops) | ex Uber(Careem) | Ola Cabs | Scaleway | Zolve

3yr •   
3yr Visible to everyone

Most of the installation documentation out there for implementing Istio Service mesh in AWS EKS lets you create a Classic Load Balancer and not an Application Load Balancer in AWS.  
Sharing a blog, that will let any DevOps/SRE's create an Istio Service Mesh that can run production workloads which can serve a high throughput of hundreds or thousands of requests per minute.

This blog is written based on inspiration from this AWS blog https://lnkd.in/gJ29zsFW.   
Made some major changes,(mentioned below are the main two changes that were done) which are not discussed in the original blog to make the Istio set up to be Production-ready in AWS and also made the implementation steps easier.

1\. added additional steps for implementing internal ALB with Istio Gateway.  
2\. using the same ALB to route traffic to multiple applications with different subdomain DNS names.

Just sharing a snippet of the main points discussed: 

1\. expose multiple applications via Internet-facing Application Load Balancer(ALB) using Istio.  
2\. expose applications via Internal Load Balancer for calls that stay within V.P.C and are not exposed over the internet, internal ALBs are needed for exposing any internal dashboards that shouldn't be accessed outside the world and should be accessed from inside the office network only.  
3\. routing traffic to multiple services using a single ALB Ingress attached with a wildcard SSL using Istio Gateway.  
4\. implement mTLS to encrypt traffic from ALB to Istio Gateway as well so SSL termination happens at the Istio Gateway level, not at the ALB level.

\#sre \#devops \#istio \#aws \#knowledgesharing \#servicemesh  
…see more

Istio Service Mesh with ALB in EKS

link.medium.com

\=== POST 312 \===  
Amit Raj  
View Amit Raj’s profile  
   
• 1st  
Senior Engineering Leader | Generative AI | Cloud SaaS | FinTech & Enterprise Scale

3yr •   
3yr Visible to everyone

SideCar and Service Mesh : 101

SideCar and Service Mesh : 101

blog.devgenius.io

\=== POST 313 \===  
Arpit Bhayani  
View Arpit Bhayani’s profile  
   
• 2nd  
Principal Engineer II at Razorpay • databases • ex-Staff Engineer at GCP Memorystore and GCP Dataproc • creator of DiceDB • built and sold Profile.fyi • ex-Amazon Fast Data and DoE Unacademy

4yr •   
4yr Visible to everyone

Spotify's outage that happened on March 8th, happened because of an outage faced by Google Traffic Director that they use for Service Discovery and routing traffic to relevant nodes.

As a fix, they rolled out a configuration that now uses DNS-based routing instead of using xDS (Service Mesh) routing offered by the Traffic Director.

Instead of DNS being the culprit, this time it came to the rescue 💪‍

Here's a detailed video explaining what happened: https://lnkd.in/gsjtswpQ

Subscribe to my YT Channel for more \#AsliEngineering videos: https://lnkd.in/g4dnhY38

\#Spotify \#Downtime \#Engineering  
…see more

\=== POST 314 \===  
sukhad anand  
View sukhad anand’s profile  
   
• 2nd  
Senior Software Engineer @Google | Techie007 | Opinions and views I post are my own

3yr •   
3yr Visible to everyone

Snapchat went down yesterday i.e 30 September 2022\. I don’t have the details of the reasons why. But, let’s explore about Snapchat architecture on how it went from being a monolith to a microservices-based architecture.

1\. A monolith is one single big fat service containing all the code and serving all the requests. Whereas, microservice-based architecture consists of many small services interacting with each other or even with outside requests.

2\. The first question is why they wanted to do this shift.? As the snap engineering team started to grow, different engineering teams wanted to function independently, They wanted to own architecture and also limit the blast radius in an outage. 

3\. This was not an easy task. There were many elements of their underlying infrastructure that needed to be considered: network topology, authentication, cloud resource provisioning, deployment, logs, metrics, traffic routing, rate limiting, and staging vs. production environments.

4\. They brainstormed a layered architecture to achieve the above. It encompassed networking, identity, provisioning, deployments, separation of business logic from infrastructure via Docker containers, and orchestration via Kubernetes. 

5\. But, as simple as it sounds, the task is not that simple. If you create multiple services, you need to take care about each of the service’s configuration. How will they interact with each other ? Security controls for each service.

6\. To make their tasks simple, they started using Envoy, an open-source framework developed by Lyft and now used across multiple different organizations. They created a service mesh with Envoy as a sidecar container running alongside the main service and handling all the communications between services. All the requests that came went through the envoy, ensuring security. Also, this helped in easy configuration management for different services discovery.

7\. Envoy would enforce TLS and publish metrics on all inbound and outbound traffic. Through this, they could guarantee that all requests between services were secure and observable.

8\. They wanted to minimize the number of services that are exposed to the Internet. This gives a first level of defense in the event of vulnerabilities, similar to what on-premises network topologies achieve with physical firewalls. They designed a shared, internal, regional network for our microservices. Services within the same region can communicate without going over the public Internet. No external traffic source could communicate directly with the internal network. In each region, only a single system would be deployed exposed to the Internet: API Gateways. All the external calls would come through it and then routed to the required service.

\_

Subscribe to my youtube channel: https://lnkd.in/eS-vkqi3  
Subscribe to my medium: https://lnkd.in/dda\_r2au  
Let's have an informal chat on Twitter: https://lnkd.in/eje\_RpzF

…see more

\=== POST 315 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗪𝗵𝗮𝘁 𝗶𝘀 𝗦𝗲𝗿𝘃𝗶𝗰𝗲 𝗠𝗲𝘀𝗵?

A Service Mesh is a dedicated infrastructure layer for managing microservice communication which controls how different parts of an application share data with one another. It helps to manage and control the communication between microservices and can provide features such as traffic management, service discovery, and security. A service mesh typically 𝗰𝗼𝗻𝘀𝗶𝘀𝘁𝘀 𝗼𝗳 𝗮 𝗻𝗲𝘁𝘄𝗼𝗿𝗸 𝗼𝗳 𝘀𝗺𝗮𝗹𝗹, 𝗹𝗶𝗴𝗵𝘁𝘄𝗲𝗶𝗴𝗵𝘁 𝗽𝗿𝗼𝘅𝘆 𝘀𝗲𝗿𝘃𝗲𝗿𝘀 that are deployed alongside each service. These proxies mediate all communication between microservices and can be configured to apply policies such as circuit breakers, rate limiting, and authentication.

In the microservice architecture, you have often a lot of chatty services that talk to each other, requesting and responding to different data. But, what if some service gets overloaded with requests? This is the place where a 𝗦𝗲𝗿𝘃𝗶𝗰𝗲 𝗠𝗲𝘀𝗵 comes in. An instance of a proxy is typically collocated with each microservice (this pattern is known as 𝘁𝗵𝗲 𝗦𝗶𝗱𝗲𝗰𝗮𝗿 𝗽𝗮𝘁𝘁𝗲𝗿𝗻). A Service Mesh is very functional after it has been set up. A comparable pool of instances is retrieved by the mesh from a service discovery endpoint. It makes a request to a particular service instance and logs the response's delay and type. Based on a variety of considerations, including the observed latency for recent requests, it selects the instance that is most likely to respond quickly.

Some 𝗲𝘅𝗮𝗺𝗽𝗹𝗲𝘀 𝗼𝗳 𝘀𝗲𝗿𝘃𝗶𝗰𝗲 𝗺𝗲𝘀𝗵𝗲𝘀 include:

🔹 𝗜𝘀𝘁𝗶𝗼: an open-source service mesh that provides traffic management, service discovery, and security features.

🔹 𝗟𝗶𝗻𝗸𝗲𝗿𝗱: an open-source service mesh that is designed to be lightweight and easy to operate.

🔹 𝗘𝗻𝘃𝗼𝘆: an open-source service mesh developed by Lyft, designed to be highly modular and extensible. 

🔹 𝗔𝗪𝗦 𝗔𝗽𝗽 𝗠𝗲𝘀𝗵: a service mesh for Amazon Web Services (AWS) that integrates with other AWS services such as ECS and Fargate.

🔹 𝗖𝗼𝗻𝘀𝘂𝗹 𝗖𝗼𝗻𝗻𝗲𝗰𝘁: a service mesh from HashiCorp that provides traffic management and service discovery features, and integrates with the Consul service registry.

Back to you, have you used service mesh before?

Image source: Microsoft.

\_\_\_\_\_\_\_  
If you like my posts please follow me Dr. Milan Milanović and hit the 🔔 on my profile to get a notification for all my new posts.

Grow with me 🚀\!

\#technology \#softwareengineering \#programming \#techworldwithmilan \#microservices  
…see more

\=== POST 316 \===  
Matthew B.  
View Matthew B.’s profile  
   
• 2nd  
Data Scientist | AI Product | LinkedIn Learning Instructor

3yr •   
3yr Visible to everyone

Starting to use Docker in Data Science?

I've been using it more as a data scientist. And for ML engineering. It's a literal game changer. And a cheat code.

Its very useful for ML deploying models. 

Things I've found useful:   
✅ Deployment Across Different Systems and Environments.   
✅ Scalability. Very useful if improving resource utilization.   
✅ Less Dependency Conflicts.

Common Use Cases:  
✅ Deploying an ML API Endpoint   
✅ A/B Testing Different Models Efficiently   
✅ Multi-Model Chaining

Here's a cheat sheet to help get you started. 

What are your thoughts?

\#datascience \#datalife360 \#vdsml \#machinelearning \#docker  
…see more

Docker for Beginners

\=== POST 317 \===  
Matt Gray  
View Matt Gray’s profile  
   
• 2nd  
Founder & CEO, Founder OS | Proven systems to grow a profitable audience with organic content.

3yr •   
3yr Visible to everyone

10 Google Chrome extensions that will supercharge your learning (all free):

10 Google Chrome extensions to supercharge your learning:

\=== POST 318 \===  
Marc van Neerven  
View Marc van Neerven’s profile  
   
• 2nd  
🦋 Chief Transformation Officer | Fractional CTO | AI Mind, SaaS Soul, Human Heart

3yr •   
3yr Visible to everyone

Monoliths, Microservices, Modular Monoliths? Native Cloud to the rescue\!

If vendor lock-in is Public Enemy No. 1 for you, I would say: read David Linthicum's "Get used to cloud vendor lock-in".

In my recent post (link in comments), I mentioned that startups should not start with Microservices, because of the extra complexity.

The post went viral.   
I referred to the term 'Modular Monolith' (not a new concept), and listed a few aspects that help you create code that:

✅ allows for splitting up later  
✅ has great discoverability  
✅ allows rapid onboarding  
✅ allows for scaling out  
✅ minimizes dependencies

There's no silver bullet, and there are many factors that define a startup's approach, but let's focus on greenfield development here, and make it really practical.

And I repeat: we're talking about Native Cloud here.

What I'm describing here is a setup I've successfully implemented with a couple of startups. One that is modern, simple and elegant and has all the benefits listed above. And one that fully leverages the power of Native Cloud.

💡 Going Native Cloud actually helps a lot in modularity and scalability.

Here's the setup:

📁 Static Frontend (SPA/PWA)  
A 100% static HTML/JS/CSS frontend, served directly from Cloud Storage. I've been doing this since 2019\. Combined with my favorite no-framework approach, with ESBuild and Lit Web Components, this gives an extremely fast, CDN-ready experience.

🗝️ Identity as a Service  
Using Azure ADB2C, AWS Identity Services, etc. Good for everyone, but especially for startups. Never ever again write your own login forms, authentication flows, JWT token creation, password reset flows, etc., and get corporate SSO, 2FA, Social Logins as configurable options.

🔀 API Gateway  
Apart from the benefits listed in my recent post about the Modular Monolith, an API Gateway is crucial in growing teams and specialization. Having frontend and backend fully separated, with the gateway in between, allows frontenders to work with mocked-up (but well-documented) backends, while the backend people are still working on API creation. Also, it guarantees that they don't ever have to understand the backend. 

⚙️ Serverless API   
Serverless Functions exposing a REST API.  
If you follow the stateless approach discussed in my previous post (see comments), using (consumption model) serverless is a great way to pay only for what you use, and there are many ways to avoid cold start issues.

—————

Of course, this setup provides just a few pieces of the puzzle, but the choices made are such that growth in every sense of the word is facilitated.

What do you think?

\#startups \#cto \#fcto \#monolith \#microservices \#softwaredevelopment \#softwareengineering \#serverless \#IDaaS \#APIGateway \#nativecloud \#cloudborn

🚀I provide CTO-as-a-Service to Startups and Scaleups   
💡I write about startups & the CTO life   
🔔Ring the bell on my profile to see when I post  
🔗neerventure dot com  
✒️Find me on Medium: @neerventure  
…see more

\=== POST 319 \===  
Shubham Mishra  
View Shubham Mishra’s profile  
   
• 1st  
SDE3 @ADOBE || Ex \- AMAZON

3yr •   
3yr Visible to everyone

Hi guys ,\#interviewprep \#dsa \#dsacoding Nowadays there are lots of free and paid resources to learn programming and dsa to finally become a good coder and bag offers from big giants and startup’s . Sometimes if we have a lot on our plate we get confused. Here I am sharing a few free resources which are enough to start and excel in this stream .

According to current level of understanding and practice ::

1 ) Hello World Programmer :: Don’t start with fancy things too soon and better to practise on some language(c++,java,python) then focus more on implementation .   
 a) javapoint ,gfg are good source of learning a new language.  
 b) Hackerearth notes 

2\) If-else Programmer :: After knowing basics of your favourite language , learn advanced aspects of it like stl in c++, collections in java . Start practising more on some platforms like hackerrank , codechef ,hackerearth .

 a) Hackerearth notes section is quite good and rich to learn algorithms.  
(https://lnkd.in/dddTCs4z)   
 b) Leetcode Learn Card (Read algorithms practise sample problems) (https://lnkd.in/dA3dzmkX)   
   
3\) Intuitive Programmer :: When you start looking for more hard and challenging problems ,and enjoy problem solving ,that time you should start learning advanced data structure like (fenvick tree ,segment tree ,KMP algo , Dynamic Programming ,Graphs)   
   
a)Leetcode problems and it’s discuss section is quite rich to learn graph and advanced dsa   
b) CSES problem set https://lnkd.in/d2uqBpBP  
c) CP algorithms my personal favourite https://cp-algorithms.com/ to learn different algo and understand sudo code of those .  
d) codechef , codeforces and leetcode for sharpening skills .  
e) Few youtube channel as TechDose , TakeUForward \#programming \#algorithms \#codechef \#learning   
…see more

\=== POST 320 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗛𝗼𝘄 𝗧𝗼 𝗕𝗲 𝗔𝗰𝗰𝗼𝘂𝗻𝘁𝗮𝗯𝗹𝗲?

What differentiates great leaders from others is that great leaders take responsibility for their words, actions, and results. And that is true in bad or good times. 𝗕𝗲𝗶𝗻𝗴 𝗮𝗰𝗰𝗼𝘂𝗻𝘁𝗮𝗯𝗹𝗲 𝗽𝗿𝗼𝗺𝗼𝘁𝗲𝘀 𝘁𝗿𝘂𝘀𝘁, 𝗹𝗲𝗮𝗱𝘀 𝘁𝗼 𝗯𝗲𝘁𝘁𝗲𝗿 𝗱𝗲𝗰𝗶𝘀𝗶𝗼𝗻𝘀 𝗺𝗮𝗸𝗶𝗻𝗴, 𝗮𝗻𝗱 𝗶𝗺𝗽𝗿𝗼𝘃𝗲𝘀 𝘁𝗲𝗮𝗺𝘄𝗼𝗿𝗸 𝗮𝗻𝗱 𝗰𝗼𝗹𝗹𝗮𝗯𝗼𝗿𝗮𝘁𝗶𝗼𝗻. An accountable leader is someone who takes ownership of their actions and decisions and is willing to accept the consequences of those decisions. They set clear goals and expectations, take responsibility, and provide clear communication with their team. 

Yet, making people accountable is not an easy task (in Serbian we don't even have a word for it). To achieve this, we can use 𝗧𝗵𝗲 𝗔𝗰𝗰𝗼𝘂𝗻𝘁𝗮𝗯𝗶𝗹𝗶𝘁𝘆 𝗟𝗮𝗱𝗱𝗲𝗿, created back in 2007\. by Bob Gordon. It is a tool that helps leaders to identify their level of accountability, from 1 (the least accountable to 8 (the most accountable):

𝟭. 𝗨𝗻𝗮𝘄𝗮𝗿𝗲: The individual or organization is not aware of the problem or issue ("I don't know").

𝟮. 𝗕𝗹𝗮𝗺𝗲 𝗼𝘁𝗵𝗲𝗿𝘀: The individual or organization recognizes the problem or issue but denies responsibility ("Not my fault").

𝟯. 𝗠𝗮𝗸𝗲 𝗲𝘅𝗰𝘂𝘀𝗲𝘀: The individual or organization accepts responsibility but tries to justify their actions or decisions ("We always done it in this way").

𝟰. 𝗪𝗮𝗶𝘁 𝗮𝗻𝗱 𝗵𝗼𝗽𝗲: The individual or organization apologizes for their actions or decisions but does not take action to correct the problem ("Sorry").

𝟱. 𝗔𝗰𝗸𝗻𝗼𝘄𝗹𝗲𝗱𝗴𝗲 𝗿𝗲𝗮𝗹𝗶𝘁𝘆: The individual or organization recognizes the problem or issue, apologizes, and takes steps to correct the problem ("I should have done it").

𝟲. 𝗢𝘄𝗻 𝗶𝘁: The individual or organization makes a commitment to solving the problem or issue and takes action to do so ("I won't do it again").

𝟳. 𝗙𝗶𝗻𝗱 𝗮 𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻: The individual or organization follows through on their commitment to solving the problem or issue ("I will do something about it").

𝟴. 𝗧𝗮𝗸𝗲 𝗮𝗰𝘁𝗶𝗼𝗻: The individual or organization monitors and improves their actions and decisions to prevent similar problems or issues from occurring in the future ("I'm working on it").

One of those abilities that some people find elusive and difficult to master is accountability. The accountability ladder can then be used to address that. It not only offers you something to go to when discussing responsibility with your staff, but it also gives them a concrete example of what being accountable looks like.

Try to be on level 8 🚀\!

Image credits: sketchplanations.

\_\_\_\_\_\_\_  
If you like my posts please follow me Dr. Milan Milanović and hit the 🔔 on my profile to get a notification for all my new posts.

Grow with me 🚀\!

\#technology \#gettingthigsdone \#techworldwithmilan \#careers \#personaldevelopment   
…see more

\=== POST 321 \===  
Arpit Bhayani  
View Arpit Bhayani’s profile  
   
• 2nd  
Principal Engineer II at Razorpay • databases • ex-Staff Engineer at GCP Memorystore and GCP Dataproc • creator of DiceDB • built and sold Profile.fyi • ex-Amazon Fast Data and DoE Unacademy

3yr •   
3yr Visible to everyone

Spend the first 3 years of your career ensuring these to accelerate your growth ⚡️

\- become proficient in at least one stack  
\- understand infrastructure and architecture  
\- understand how your work fits into the big scheme  
\- show extreme ownership and lead  
\- help others succeed

ps: youtube.com/c/ArpitBhayani

\#AsliEngineering  
…see more

\=== POST 322 \===  
Status is online  
Hemant Pandey  
View Hemant Pandey’s profile  
   
• 1st  
Helping Software Engineers 2X their compensation | Tech Lead | Ex \- Meta, Salesforce, Tesla | Featured on Business Insider and Times Square

3yr •   
3yr Visible to everyone

“Your partner has more impact on your career than your manager”

As we navigate our professional lives, it is easy to become fixated on our managers and the impact they have on our careers. However, it is important to recognize that our partners play an equally or more important role in our professional journeys.

👉Our partners are often the ones who provide emotional support and encouragement when we are facing difficult challenges at work. They are the ones who celebrate our successes and offer a listening ear when we need to vent about work-related stress. 

👉 They are our sounding boards when we are considering a new job opportunity or a career change, and they provide valuable perspective when we are making important decisions about our professional lives.

👉 In addition to emotional support, our partners also play a crucial role in our professional development. They can help us to identify our strengths and weaknesses, and offer guidance and advice on how to improve and grow as professionals. 

👉 They can also be an important source of networking opportunities, introducing us to people in our industry or connecting us with potential employers.

👉 Furthermore, our partners can also have a significant impact on our work-life balance. They can help us to prioritize our time and energy, and ensure that we are not sacrificing our personal lives for our professional ones. 

👉They can also be a great source of motivation, encouraging us to set and achieve our professional goals.

It is important to remember that our partners are not just our significant others, but also our partners in life. They are our partners in our career journey, and they play an integral role in our success and happiness in the workplace. 

Sharing this post on our 3rd anniversary, so grateful to have a partner like Vaashu in my life 😀

\#coding \#programming \#softwareengineering \#relationships  
…see more

\=== POST 323 \===  
Matt Gray  
View Matt Gray’s profile  
   
• 2nd  
Founder & CEO, Founder OS | Proven systems to grow a profitable audience with organic content.

3yr •   
3yr Visible to everyone

YouTube is free education.

But 98% of people don't know the best professors on its virtual campus.

Here are the top 9 channels to accelerate your learning:  
…see more

Top 9 YouTube Channels To Accelerate Your Learning:

\=== POST 324 \===  
Ben Meer  
View Ben Meer’s profile  
   
• 3rd+  
The Systems Guy • Follow me for systems on health, wealth, and free time ⚡ Cornell MBA • 2M+ audience

3yr •   
3yr Visible to everyone

How to be more productive (without burning out).  
   
The 3-3-3 Method:  
   
Source: I learned of 3-3-3 from Oliver Burkeman. I highly recommend his book, Four Thousand Weeks.  
…see more

\=== POST 325 \===  
Milan Jovanović  
View Milan Jovanović’s profile  
   
• 2nd  
Practical .NET and Software Architecture Tips | Microsoft MVP

3yr •   
3yr Visible to everyone

Want to be a better software engineer in 2023?

Here are 5 simple tips to help you get there:  
1\. Keep learning and acquiring new skills  
2\. Invest in code quality  
3\. Work on complex systems  
4\. Be comfortable in the cloud  
5\. Take care of yourself

𝗞𝗲𝗲𝗽 𝗟𝗲𝗮𝗿𝗻𝗶𝗻𝗴 𝗔𝗻𝗱 𝗔𝗰𝗾𝘂𝗶𝗿𝗶𝗻𝗴 𝗡𝗲𝘄 𝗦𝗸𝗶𝗹𝗹𝘀

The field of software engineering is constantly evolving, so it's important to stay up-to-date with new technologies and best practices.

We have a new .NET release every year, and it's easy to get lost in the latest news. How I stay up to date is through online courses, attending conferences and meetups, or working on personal projects.

𝗜𝗻𝘃𝗲𝘀𝘁 𝗜𝗻 𝗖𝗼𝗱𝗲 𝗤𝘂𝗮𝗹𝗶𝘁𝘆

In addition to writing clean and readable code, it's important to also consider the overall quality of your code.

This includes things like performance, security, and maintainability. By writing high-quality code, you'll be able to build systems that are more reliable, scalable, and easier to maintain over time.

Investing in code quality will pay dividends in the later stages of any project.

𝗪𝗼𝗿𝗸 𝗢𝗻 𝗖𝗼𝗺𝗽𝗹𝗲𝘅 𝗦𝘆𝘀𝘁𝗲𝗺𝘀

If you aspire to be a senior engineer or software architect, you have to work on complex systems. You need to be in a position to solve the toughest problems.

What do I consider to be a complex system?

That's difficult to say, but here are some rough guidelines:

• Microservices  
• Event-driven systems  
• High performance systems

If you are working in a business domain with many domain rules, I consider that a complex system also.

𝗕𝗲 𝗖𝗼𝗺𝗳𝗼𝗿𝘁𝗮𝗯𝗹𝗲 𝗜𝗻 𝗧𝗵𝗲 𝗖𝗹𝗼𝘂𝗱

The cloud is here to stay, and you should be familiar with at least one of the major cloud providers: Azure, AWS, or GCP.

Most of them give you free credits to get started and explore the services they offer.

I stayed away from cloud development for too long in my career, and now I wish I started sooner.

𝗧𝗮𝗸𝗲 𝗖𝗮𝗿𝗲 𝗢𝗳 𝗬𝗼𝘂𝗿𝘀𝗲𝗹𝗳

Being a software engineer is mentally and physically demanding, and it's important to take care of yourself in order to maintain a healthy work-life balance.

This includes getting enough sleep, eating well, and taking breaks when needed.

Taking care of yourself can also help you stay focused and productive in your work.

𝗪𝗵𝗮𝘁 𝗜'𝗺 𝗗𝗼𝗶𝗻𝗴 𝗧𝗼 𝗠𝗮𝗸𝗲 𝟮𝟬𝟮𝟯 𝗔𝗺𝗮𝘇𝗶𝗻𝗴

I've found the simplest rule to always make progress is taking action. I try to make a small step forward every day. And when I look back on the year, I realize I made a lot of progress.

Where I failed most in 2022 was taking care of myself, and this will be one of my main improvement points.

If you enjoyed this post, I share practical tips like these every Saturday in my weekly newsletter.

Join more than 7800 engineers who have already subscribed:

https://lnkd.in/dMDPXuUh  
…see more

\=== POST 326 \===  
Ahmad Awais  
View Ahmad Awais’ profile  
   
• 2nd  
Founder & CEO ⌘ CommandCode.ai x Langbase ❯ Award-winning Open Source Eng ❯ Angel Investor ❯ NASA Ingenuity Code ❯ Google Advisory Board ❯ Ex VP DX ❯ Microsoft MVP ❯ 5x GitHub Stars Award

3yr •   
3yr Visible to everyone

Confused about servers? — my team's got you covered\!

\=== POST 327 \===  
Mohamed A.  
View Mohamed A.’s profile  
   
• 2nd  
Staff Platform Engineer | Helping startups, scale-ups and mid/enterprises build production-grade infrastructure | Opinions are my own

3yr •   
3yr Visible to everyone

You can easily get lost with the millions of GitHub repositories out there. 

𝐇𝐞𝐫𝐞 𝐚𝐫𝐞 𝐚 𝐜𝐮𝐫𝐚𝐭𝐞𝐝 𝐥𝐢𝐬𝐭 𝐨𝐟 𝐆𝐢𝐭𝐇𝐮𝐛 𝐫𝐞𝐩𝐨𝐬𝐢𝐭𝐨𝐫𝐢𝐞𝐬 𝐭𝐡𝐚𝐭 𝐰𝐢𝐥𝐥 𝐫𝐞𝐚𝐥𝐥𝐲 𝐡𝐞𝐥𝐩 𝐲𝐨𝐮 𝐭𝐨 𝐚𝐝𝐯𝐚𝐧𝐜𝐞 𝐲𝐨𝐮𝐫 𝐜𝐚𝐫𝐞𝐞𝐫 𝐢𝐧 𝐒𝐨𝐟𝐭𝐰𝐚𝐫𝐞 𝐄𝐧𝐠𝐢𝐧𝐞𝐞𝐫𝐢𝐧𝐠, 𝐃𝐞𝐯𝐎𝐩𝐬, 𝐒𝐑𝐄 𝐚𝐧𝐝 𝐦𝐨𝐫𝐞\! 📚

1\. A list of programming tutorials in which aspiring software engineers learn how to build an application from scratch. 

📌 (https://lnkd.in/enxAaRv4)

2\. Contains questions and exercises on various technical topics related to DevOps and SRE

📌 (https://lnkd.in/eqR-Y5Pn)

3\. Useful resources for Site Reliability Engineering and DevOps

📌 (https://lnkd.in/eRJkKPmE)

4\. Learn how to design large-scale systems

📌 (https://lnkd.in/e4q\_gmGK)

5\. A collections of Linux SysAdmin/DevOps questions to help you getter a better understanding of Linux

📌 (https://lnkd.in/ejnAuQtY)

6\. A study guide for Software Engineers looking to get better at Data Structures & Algorithms

📌 (https://lnkd.in/eHfVhAHA)

7\. A collection of (mostly) technical things every developer should aim to know

📌 (https://lnkd.in/eYvUChpG)

8\. Community driven roadmaps, articles and resources for Devs, Architects, QA and DevOps and more\!

📌 (https://lnkd.in/ew87589P)

9\. Curated questions and answers to test your knowledge on Linux

📌 (https://lnkd.in/eTjMHBHq)

10\. Curated collection of resources for frontend web developers

📌 (https://lnkd.in/ekShjrRQ)

11\. Learn Software Architecture, Design patterns, DDD, SOLID principles and good software practices

📌 (https://lnkd.in/eK4vFGf9)

12\. A set of guidelines for best practices, styles and methods for various programming languages.

📌 (https://lnkd.in/ewc85mED)

\#softwareengineering \#coding \#systemdesign \#devops \#sre \#github  
…see more

\=== POST 328 \===  
Pradeep Pandey  
View Pradeep Pandey’s profile  
   
• 2nd  
Co-founder at AI insights | AI educator | Web developer

3yr •   
3yr Visible to everyone

80% programmers use VS Code. But their Productivity Suck.

Here are the top 9 VS code extensions to take your productivity to next level.

1\. CodeSnap

⇨ Quickly allows you to create screenshots of your code by simply highlighting the respective snippet within your project.  
👉 https://lnkd.in/di\_hxjGB

2\. Live Server

⇨ When you write your HTML, CSS, or JavaScript file you can press "Go Live" at the bottom of your VsCode window and it will automatically add your changes on a webpage without any reloads, etc.  
👉 https://lnkd.in/d35BTMZK

3\. Colorize

⇨ Colorize visualizes color variables by highlighting them with their color value. This is a handy timesaver for translating hex codes and variable names.  
👉 https://lnkd.in/dj39Nmag

4\. Prettier

 ⇨ For those of you that don't know, Prettier is an opinionated code formatter for Javascript/Typescript, HTML, JSX, and more.  
👉 https://lnkd.in/d8-Gerdu

5\. Project Manager

→ It helps you to easily access your projects, no matter where they are located. Don't miss those important projects anymore.  
👉 https://lnkd.in/dGFg2PNQ

6\. Tabnine

→ Tabnine serves up suggestions for code completions right in Visual Studio Code, with no distractions and no downtime.  
👉 https://lnkd.in/dzyw8\_N6

7\. ESLint

This extension is used for analyzing your JavaScript code and fixing the errors in them. You can install and edit your JS code to fix the errors pointed out.   
👉 https://lnkd.in/dd752zDg

8\. GitLens

This extension is used for getting information from a Git source that can be edited in the VS environment.   
👉 https://lnkd.in/de8GJipb

9\. JavaScript (ES6) Code Snippets

This extension is used for setting shortcut triggers for JavaScript code that can be used to invoke a full code instead of typing out code on each instance.   
👉 https://lnkd.in/dPW78G8M

Thanks for reading.

Follow ➡️ Pradeep Pandey For More ✨

Hashtags :  
\#vscode \#extensions \#productivity \#vscodeextensions \#javascriptdeveloper \#learn \#git \#coder \#code \#web \#website \#javascriptdeveloper \#development \#webdevelopment \#webdeveloper \#frontend \#backend \#frontenddeveloper \#backenddeveloper \#html5 \#html \#css3 \#css \#javascript \#js \#reactjs  
 

…see more

\=== POST 329 \===  
Pradeep Pandey  
View Pradeep Pandey’s profile  
   
• 2nd  
Co-founder at AI insights | AI educator | Web developer

3yr •   
3yr Visible to everyone

There are millions of repositories on GitHub. Only a few will help you grow.

Here are 12 awesome GitHub repositories to save you 15+ hrs every week.

1\. Useful visual roadmap to becoming a web developer in 2023\.  
👉 https://lnkd.in/dVHKBP2k

2\. Useful lists about all kinds of interesting topics and technologies.  
👉 https://lnkd.in/dG6eeT8r

3\. Freely available programming books for all technologies.  
👉 https://lnkd.in/d8zFbDcr

4\. Biggest collection of free public APIs for any project.  
👉 https://lnkd.in/d3UGy-B8

5\. A collection of awesome browser-side JavaScript libraries, resources and shiny things.  
👉 https://lnkd.in/dmsQrdyq

6\. Curated interview preparation materials for busy engineers. Ace your programming interviews.  
👉 https://lnkd.in/dHpj7tef

7\. Explanations of Algorithms and data structures in JavaScript with useful links.  
👉 https://lnkd.in/dvDFZq92

8\. Explanation of 33 Concepts Every JavaScript Developer Should Know.  
👉 https://lnkd.in/d9-Zry6x

9\. A Collection of app ideas for your next project.  
👉 https://lnkd.in/dJ9squy9

10\. A list of the top websites for programmers.  
👉 https://lnkd.in/dMkFJgGk

11\. Curated list of design and UI resources including stock photos, templates, frameworks, and more.  
👉 https://lnkd.in/deXXW-kq

12\. A collection of awesome browser-side JavaScript libraries, resources and useful things.  
👉 https://lnkd.in/dmsQrdyq

Thanks for reading.

Follow Pradeep Pandey For More ✨

Hashtags :  
\#github \#repository \#javascriptdeveloper \#learn \#git \#coder \#code \#web \#website \#javascriptdeveloper \#development \#webdevelopment \#webdeveloper \#frontend \#backend \#frontenddeveloper \#backenddeveloper \#html5 \#html \#css3 \#css \#javascript \#js \#reactjs   
…see more

\=== POST 330 \===  
Status is reachable  
Sumit Bhanushali  
View Sumit Bhanushali’s profile  
   
• 1st  
Lead Engineer (SDE-3) @SprintMoney | Ex-Frappe | Ex-Servify

3yr •   
3yr Visible to everyone

When upgrading your backend system, databases are the first thing we should scale as they are usually the main bottleneck of a system. First step should be to scale the database vertically and upon hitting the limit of scaling vertically, we can move to scaling the database horizontally. As databases are ready heavy, we can adopt the Master Slave Replication strategy which is the easiest and efficient way to scale a database. 

Check comment for detailed blog on how to develop intuition for upgrading your Backend System👇

\#database \#systemdesign   
…see more

\=== POST 331 \===  
Mohamed A.  
View Mohamed A.’s profile  
   
• 2nd  
Staff Platform Engineer | Helping startups, scale-ups and mid/enterprises build production-grade infrastructure | Opinions are my own

3yr •   
3yr Visible to everyone

𝐋𝐨𝐠 𝐩𝐚𝐫𝐬𝐢𝐧𝐠 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐢𝐧 𝐋𝐢𝐧𝐮𝐱

Over the weekend, I was working on my log parsing skills and wanted to use “awk” & “grep” simultaneously to search for a specific pattern in a log. I stumbled upon an incredibly helpful cheatsheet. Hope you can find it of use too\!

Log parsing commands are handy for:  
🔹 When looking for specific patterns in a text/log file in a Linux machine (grep)  
🔹 Analysing network packets (ngrep)  
🔹 Replacing specific strings in a file (sed)  
🔹 Sorting contents of a file \- numerically or alphabetically (sort)  
🔹 Comparing differences between files (diff)  
🔹 Extracting fields from delimited logs and processing them (awk)

Image credits: Thomas Roccia

Which of these commands do you use daily?

\#linux \#logs \#networking   
…see more

\=== POST 332 \===  
Status is reachable  
Sumit Bhanushali  
View Sumit Bhanushali’s profile  
   
• 1st  
Lead Engineer (SDE-3) @SprintMoney | Ex-Frappe | Ex-Servify

3yr •   
3yr Visible to everyone

ACID properties in relational databases are important but are easy to forget. 

Everytime I want to revise them I end up on different resource and have to remap it with my level of understanding. So today I decided to write a blog on it so that I can refer it whenever I have to. 

Do give it a read, let me know if you found it helpful and have any feedback

https://lnkd.in/dQNTfVyQ

 \#database \#systemdesign \#relationaldatabases   
…see more

Never forget ACID again\!\!

sumitbhanushali.hashnode.dev

\=== POST 333 \===  
Arpit Bhayani  
View Arpit Bhayani’s profile  
   
• 2nd  
Principal Engineer II at Razorpay • databases • ex-Staff Engineer at GCP Memorystore and GCP Dataproc • creator of DiceDB • built and sold Profile.fyi • ex-Amazon Fast Data and DoE Unacademy

3yr •   
3yr Visible to everyone

Reminder: It will take you 10 years to realize how great our college curriculum is and how critical the core Computer Science subjects are.

Do not get misguided by these "EdTech cum SalesTech" startups and influencers. Everything at scale just boils down to

\- Operating system concepts: Mutex, Semaphores, Critical Sections, Thread, Sockets, etc

\- Database Internals: Query optimization of Database

\- Distributed Systems: Need I say anything here

\- Computer Architecture: To understand why vertical scaling has a limit, the importance of page faults, cache lines

\- Networking: Securing infra, optimizing routing, BGP protocol, CDN, TCP, UDP, etc.

\- Multimedia Processing: video encoding, codec conversions, image processing, RTMP, etc

to just name a few

Core CS subjects are more important in the real world. DSA might be there for interviews, but the core CS subjects are mighty critical while at work.

Never neglect them. It will take you a decade to realize ki ya sab to college me hi padha tha.

\#Engineering \#ComputerScience \#AsliEngineering   
…see more

\=== POST 334 \===  
👨🏻‍💻 Nitsan Cohen  
View 👨🏻‍💻 Nitsan Cohen’s profile  
   
• 1st  
ML & LLM Engineer @ Viewz | Python & React | System Design

3yr •   
3yr Visible to everyone

Types or Interfaces? That is the question.

In TypeScript, both interfaces and types are used to describe the shape of an object or a function signature. However, there are some key differences between the two that are important to understand.

1\. Objects and Functions: Both interfaces and types can be used to define the shape of an object or a function, but the syntax is different. Look in the attached code block snippet 1 and 2 for examples of how to define an interface and a type respectively.

2\. Other Types: Type aliases can also be used to define other types such as primitives, unions, and tuples. Look in the attached code block snippet 3 for examples of how to define other types using type aliases.

3\. Extending: Both interfaces and types can be extended, but the syntax is different. Additionally, note that an interface and type alias can be used together. Look in the attached code block snippet 4 and 5 for examples of how to extend interfaces and type aliases respectively.

4\. Implementing: A class can implement an interface or type alias in the same way. However, a class and interface are considered static blueprints, so they cannot implement or extend a type alias that names a union type. Look in the attached code block snippet 6, 7, 8 for examples of how to implement interfaces and type aliases respectively.

5\. Declaration Merging: Unlike a type alias, an interface can be defined multiple times, and will be treated as a single interface (with members of all declarations being merged). Look in the attached code block snippet 9 for an example of how to merge interface declarations.

In conclusion, both interfaces and types are powerful tools in TypeScript that can be used to define the shape of objects and functions. However, there are some key differences between the two, such as syntax, types that can be defined, extending, implementing, and declaration merging. It is important to understand these differences in order to make informed decisions when designing your application.

\#typescript \#webdevelopment \#developer   
…see more

\=== POST 335 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗪𝗵𝘆 𝗶𝘀 𝗖𝗿𝗶𝘁𝗶𝗰𝗮𝗹 𝗧𝗵𝗶𝗻𝗸𝗶𝗻𝗴 𝗮 𝗚𝗮𝗺𝗲 𝗖𝗵𝗮𝗻𝗴𝗲𝗿 𝗙𝗼𝗿 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿𝘀?

I was often asked if doing a Ph.D. was worth it, taking into account that I left academia and went to the industry. The clear answer is yes because there I learned some skills that as a developer I wouldn't have, such as, how to write, how to collaborate, how to do critical thinking, etc. By far the most important skill I learned is how to do 𝗰𝗿𝗶𝘁𝗶𝗰𝗮𝗹 𝘁𝗵𝗶𝗻𝗸𝗶𝗻𝗴. And it is also something coming deep from my nature, as saying: "we are always doing it in this way", is usually not a good enough explanation for me. 

In our industry, we always need to test the benefits and drawbacks of different technologies, architectural approaches, etc. It is very important to know how to approach and test those options and make proper decisions. Critical thinking is a way to process information before you get an answer or conclusion. Critical thinking and problem-solving are the things that make good developers great. 

Usually, a process of critical thinking goes in the following steps:

𝟭. 𝗜𝗱𝗲𝗻𝘁𝗶𝗳𝘆 𝘁𝗵𝗲 𝗽𝗿𝗼𝗯𝗹𝗲𝗺

𝟮. 𝗔𝗻𝗮𝗹𝘆𝘇𝗲 𝘁𝗵𝗲 𝗽𝗿𝗼𝗯𝗹𝗲𝗺 𝗳𝗿𝗼𝗺 𝗱𝗶𝗳𝗳𝗲𝗿𝗲𝗻𝘁 𝗽𝗲𝗿𝘀𝗽𝗲𝗰𝘁𝗶𝘃𝗲𝘀 𝗮𝗻𝗱 𝗱𝗶𝘀𝗰𝗼𝘃𝗲𝗿 𝘁𝗵𝗲 𝗳𝗮𝗰𝘁𝘀

𝟯. 𝗖𝗵𝗮𝗹𝗹𝗲𝗻𝗴𝗲 𝘆𝗼𝘂𝗿 𝗯𝗶𝗮𝘀𝗲𝘀, 𝗯𝘆 𝗮𝘀𝗸𝗶𝗻𝗴 𝘆𝗼𝘂𝗿𝘀𝗲𝗹𝗳 𝘄𝗵𝗲𝘁𝗵𝗲𝗿 𝘆𝗼𝘂’𝗿𝗲 𝗺𝗮𝗸𝗶𝗻𝗴 𝗮𝘀𝘀𝘂𝗺𝗽𝘁𝗶𝗼𝗻𝘀

𝟰. 𝗛𝘆𝗽𝗼𝘁𝗵𝗲𝘀𝗶𝘇𝗲 𝗽𝗼𝘀𝘀𝗶𝗯𝗹𝗲 𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻𝘀 𝗯𝗮𝘀𝗲𝗱 𝗼𝗻 𝗮𝗻 𝘂𝗻𝗱𝗲𝗿𝘀𝘁𝗮𝗻𝗱𝗶𝗻𝗴 𝗼𝗳 𝘁𝗵𝗲 𝗽𝗿𝗼𝗯𝗹𝗲𝗺 𝗮𝗻𝗱 𝘆𝗼𝘂𝗿 𝗽𝗮𝘀𝘁 𝗸𝗻𝗼𝘄𝗹𝗲𝗱𝗴𝗲

𝟱. 𝗧𝗲𝘀𝘁 𝗮𝗻𝗱 𝗰𝗼𝗺𝗽𝗮𝗿𝗲 𝘁𝗵𝗲 𝗲𝗳𝗳𝗲𝗰𝘁𝗶𝘃𝗲𝗻𝗲𝘀𝘀 𝗼𝗳 𝗲𝗮𝗰𝗵 𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻 𝗮𝗻𝗱 𝘁𝗵𝗲 𝗳𝗲𝗮𝘀𝗶𝗯𝗶𝗹𝗶𝘁𝘆 𝗼𝗳 𝗶𝗺𝗽𝗹𝗲𝗺𝗲𝗻𝘁𝗮𝘁𝗶𝗼𝗻

𝟲. 𝗦𝗲𝗹𝗲𝗰𝘁 𝗼𝗻𝗲 𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻 𝘁𝗵𝗮𝘁 𝗳𝗶𝘁𝘀 𝘆𝗼𝘂𝗿 𝗰𝗿𝗶𝘁𝗲𝗿𝗶𝗮

𝟳. 𝗖𝗼𝗺𝗺𝘂𝗻𝗶𝗰𝗮𝘁𝗲 𝗿𝗲𝘀𝘂𝗹𝘁𝘀 𝘁𝗼 𝗮𝘀 𝘄𝗶𝗱𝗲 𝗮 𝗽𝗼𝗼𝗹 𝗮𝘀 𝗽𝗼𝘀𝘀𝗶𝗯𝗹𝗲 𝗮𝗻𝗱 𝘁𝗮𝗸𝗲 𝗮𝗰𝘁𝗶𝗼𝗻𝘀

The most important step 2\. can be approached by asking some good questions:

✅ Is this necessary to do at all?  
✅ Are we solving the right problem?  
✅ Are we solving the problem in the right way?  
✅ What goal do we want to achieve with this?  
✅ Can we take another look at this?  
✅ How we can break big problems into smaller ones?  
✅ How do I know I succeeded?  
✅ Is this solution good enough?

These are some examples of questions you can ask. Not all the questions you ask yourself have to have an answer. Talk about such issues with your management, the owner of the business, or the client. Understanding what problem you are fixing, why, and whether this does not cause new issues elsewhere is crucial.

What differentiates critical thinkers from others, they are curious, drop less useful information and use the right ones, use reliable sources, listen actively, communicate effectively, and have empathy too.

\#softwareengineering \#techworldwithmilan \#productivity \#personaldevelopment   
…see more

\=== POST 336 \===  
Abhinav S.  
Abhinav S.  
View Abhinav S.’s profile  
   
• 2nd  
Software Engineer 2 @Linkedln | Ex \- @Media.net | Master @ CodeForces | 6 ⭐ @Code Chef | Former SWE Intern at Google

3yr •   
3yr Visible to everyone

🚀Preparation Strategy For Google interview   
Leetcode:

1\. Try to do daily Leetcode challenges. It helps you in being consistent and also covers variety of problems.

2\. Top 100 questions by frequency.

3\. Top 75 LC curated: https://lnkd.in/dD5MmEks

4\. Out of which most of them were rated Hard , as I was comfortable in easy/medium ones. But you should focus on easy/medium ones. It would be more helpful. Give as many mock interviews as possible.

5\. Try to solve Leetcode google tagged questions.

6\. Crckg the Cdng Intriew book.

Few Tips:

1\. Try to solve a problem by yourself, even if you are not able to come- up with an optimal solution.

2\. Think about time and space complexity of your solution. Identify sections which can be optimised and think of a better solution/ data structure.

3\. Check Leetcode Solutions/ Refer Discuss section. After understanding the approach, try to implement it yourself without taking a look at code. 

4\. This would help you in really understanding the concept.  
Try to beat 90% of solutions by runtime.

System Design:

1\. Book: DDIA (MUST READ if targeting Google)

2.Book: System Design \_Interview by Alex Xu

3.System Design Primer by Donne Martin  
4.Courses \- Gr\_k\_i\_g the System Design and Gr\_k\_i\_g the Ad\_\_nced System Design.

Behavioural:

1\. Understand various Leadership principles.

2\. Go through your Resume and write stories following STAR approach. 

3\. Your story should project at-least one of the attribute such as taking lead, resolving conflicts, dealing with ambiguity etc..

4.Read, Rehearse and Repeat.

Time Management: I had a decent work-load in my day job. So spent \~2 hours on average on a working day and 4-5 hours on weekends/holidays.

Make sure you cover the following topics : 

1\. UnionFind  
2\. Trie  
3\. Cycle Detection  
4\. Intervals  
5\. Segment Tree/Fenwick Tree  
6\. Graph distance   
7\. Trie  
8\. Randomisation problems   
9\. Topological sort  
10\. DFS/BFS  
11\. 2-D Matrix Prefix Sum  
12\. Dijkstra/Bellman Ford/ Floyd Warshall/ Kruskal's Minimum Spanning Tree.  
I hope you learned something new from my experience and even got the confidence.   
\#google \#data \#interview \#strategy \#share \#experience \#dsa \#dsacoding \#leetcode \#interviewpreparation \#interviewquestions \#interview \#hiring \#hiringalerts \#leadership \#design \#job   
…see more

\=== POST 337 \===  
Pratham Kohli  
View Pratham Kohli’s profile  
   
• 2nd  
AI Engineering @Salesforce | Writes to 450k+ (LinkedIn, Instagram) | Prev: Amazon, ServiceNow, ISRO | NIT Jalandhar | Helping you make your Dream Switch

3yr •   
3yr Visible to everyone

Given the recent situation of layoffs\! 🥲  
Don't limit your search only to MAANGA (Meta, Amazon, Apple, Netflix, Google, and Microsoft) companies. ❌

There are many fantastic companies out there in terms of:  
Pay  
Work-life balance  
Work culture  
Career growth  
and a lot more things.

Here is a list of 115+ such companies on the basis of their marketplace/field.   
Hoping this will be helpful

Mobility Companies:  
\- Ola  
\- Uber  
\- Bluesmart  
\- Meru  
\- Zoomcar  
\- Rapido

E-commerce  
\- Walmart  
\- Flipkart  
\- Myntra  
\- Tesco  
\- Target  
\- Shopsy  
\- Bloomreach  
\- Udaan  
\- Cult.fit  
\- Urban company  
\- Ajio  
\- PharmaEasy  
\- Meesho  
\- Lowe's Companies, Inc.

CRM/Workflow Management  
\- Zoho  
\- Salesforce  
\- EngageBay  
\- ServiceNow

Recruitment/ Hiring platform  
\- LinkedIn  
\- Indeed  
\- Uplers  
\- Naukri.com (Infoedge)

Collaboration tools  
\- Atlassian  
\- Asana  
\- Zoom  
\- Slack

Cloud services/Saas  
\- Oracle Cloud Infrastructure (OCI)  
\- VMware  
\- Redhat  
\- SAP Labs  
\- Hewlett Packard Enterprise (HPE)  
\- IBM  
\- BrowserStack  
\- Nutanix  
\- NetApp  
\- Tekion Corp  
\- Cohesity  
\- Rubrik

Communication  
\- Slack  
\- Zoom  
\- Twilio  
\- Twitter  
\- Airtel X labs

Advertisement  
\- media.net  
\- Adpushup  
\- Kevel

Payments / Fintech  
\- Paypal  
\- Visa  
\- Phonepe  
\- Paytm  
\- Bhartpe  
\- Cred  
\- Jupiter  
\- Slice  
\- Razorpay  
\- Zeta  
\- Rupeek  
\- ClearTax

Trading  
\- Tower research capital  
\- Upstox  
\- Groww  
\- Zerodha

Investment Banks/ Hedge funds and others  
\- De Shaw  
\- Goldman Sachs  
\- World quant  
\- Arcesium  
\- Intuit  
\- JP Morgan  
\- Morgan Stanley  
\- Wells Fargo  
\- Druva

Travel  
\- Airbnb  
\- OYO rooms  
\- MakeMyTrip  
\- Bookmytrip  
\- Expedia  
\- Groupon  
\- Booking.com  
\- Agoda

Network/Hardware  
\- Directi  
\- Qualcomm  
\- Dell  
\- VMware  
\- Nvidia  
\- Arista Networks  
\- Palo Alto Networks

Gaming Industry  
\- Dream 11  
\- Cricbuzz  
\- MPL  
\- Zynga  
\- Bluestacks  
\- Hike  
\- Games24x7

Entertainment  
\- Hotstar  
\- Flock  
\- Inmobi  
\- Sharechat

Food delivery  
\- Swiggy  
\- Zomato  
\- Dunzo

Logistics  
\- Rivigo  
\- Delhivery  
\- Pickrr  
\- Turvo  
\- Porter  
\- Vahak

Analytics  
\- Fractal  
\- Tredence  
\- Tiger Analytics  
\- Latentview   
\- MuSigma

Telecom  
\- Ericsson   
\- Nokia  
\- Tejas networks  
\- NEC  
\- Radisys

Curation credits: Nitesh Yadav

Follow Pratham Kohli for more 🙌🏻

\#hiring \#jobsearch \#layoffs \#recruitment \#microsoft \#amazon \#google \#career  
…see more

\=== POST 338 \===  
Alex N.  
View Alex N.’s profile  
   
• 2nd  
Software Engineer | Prev. @ Google

3yr •   
3yr Visible to everyone

Books I'm reading now that I'm not a junior engineer

1\. Mythical Man Month \- This book is a collection of essays that easily explains why adding more people to a late project doesn't help.

2\. Working Effectively with Legacy Code \- Legacy code can also mean your existing code base. Add tests, it makes your codebase MORE resilient because they tell you things won't change.

3\. Clean Code \- Don't read this book and immediately implement everything you see. But you'll read and walk away knowing why your functions should be small and smaller than that.

4\. Designing Data-Intensive Applications \- Read this book and you'll learn the ideas behind any large application. You will learn about CAP theorem, failover, transactions, map-reduce, and tons more reading this.

5\. Domain Driven Design \- For any product, this book will teach you how to translate that to code. Learning about repositories, value objects vs. entities, aggregates, and bounded contexts makes this book worthwhile.

6\. Design Patterns \- For anyone learning about object oriented programming, this book explains industry standard design patterns that are still used today. There's a lot and I definitely need to brush up on some.

Code is read 10x more than it's written  
So spend time learning to write code 10x better.

\---  
If you're looking to catch up on system design, take a look at ByteByteGo's System Design Interview:  
 https://lnkd.in/gqVP8pSz

\#alexcancode  
\#softwareengineer  
\#programming  
…see more

\=== POST 339 \===  
Jade Bonacolta  
View Jade Bonacolta’s profile  
   
• 2nd  
Ranked \#1 Female Creator on LinkedIn | Founder of The Quiet Rich™ | Ex-Google | Forthcoming Author | Follow me for daily life hacks

3yr •   
3yr Visible to everyone

“You can’t be normal and expect abnormal returns.”—Jeffrey Pfeffer

6 contrarian books to achieve outlier results:

6 contrarian books to achieve outlier results:

\=== POST 340 \===  
Matt Gray  
View Matt Gray’s profile  
   
• 2nd  
Founder & CEO, Founder OS | Proven systems to grow a profitable audience with organic content.

3yr •   
3yr Visible to everyone

9 Ted Talks in 9 days that will change your life:

9 Ted Talks In 9 Days That Will Change Your Life:

\=== POST 341 \===  
Status is reachable  
Tannishk Sharma  
View Tannishk Sharma’s profile  
   
• 1st  
Senior AI Product Manager | Amazon | Scaled E-commerce Products to 50M+ Users | 100 M+ Cost Savings | Fintech | Payments | Ex-Paytm, Urban company , Udaan

3yr •   
3yr Visible to everyone

So many people asking me, writing a post about it. If you are someone who wants to move into a Product Management role, I will highly recommend you to read these three books \-

1\. Cracking the PM interview by Gayle McDowell

2\. Decode and Conquer by Lewis C. Lin

3\. Hooked: How to Build Habit-Forming Products \- Nir Eyal

4\. Lean Product Playbook 

5\. Inspired 

\#productmanagement \#bookrecommendations  
\#writing \#people   
…see more

\=== POST 342 \===  
Milan Jovanović  
View Milan Jovanović’s profile  
   
• 2nd  
Practical .NET and Software Architecture Tips | Microsoft MVP

3yr •   
3yr Visible to everyone

Here are three books that made me a better software engineer:

1\. Domain-Driven Design, Eric Evans

2\. Designing Data-Intensive Applications, Martin Kleppmann

3\. The Effective Engineer, Edmond Lau

Which book left an impact on you?  
…see more

\=== POST 343 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗟𝗶𝗻𝘂𝘅 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀

A nice overview of all Linux commands, such as:

• Basic File Operations: ls, cp, mv, rm, ...  
• File Viewing: cat, less, head, tail, nl, ...  
• Dates and times: xclock, cal, date, ...  
• Network: traceroute, ifconfig, netstat, who, ...  
• Viewing Processes: ps, uptime, w, top, ...

Credits: kPastor.  
\_\_\_\_\_\_\_  
If you like my posts please follow me Dr. Milan Milanović and hit the 🔔 on my profile to get a notification for all my new posts.

Grow with me 🚀\!

\#technology \#softwareengineering \#programming \#techworldwithmilan \#linux  
…see more

\=== POST 344 \===  
Ben Meer  
View Ben Meer’s profile  
   
• 3rd+  
The Systems Guy • Follow me for systems on health, wealth, and free time ⚡ Cornell MBA • 2M+ audience

3yr •   
3yr Visible to everyone

10 documentaries that will inspire \+ motivate you in 90 mins or less:

10 documentaries that will change your mindset:

\=== POST 345 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝟭𝟱 𝗕𝗲𝘀𝘁 𝗟𝗲𝗮𝗱𝗲𝗿𝘀𝗵𝗶𝗽 𝗕𝗼𝗼𝗸𝘀 

I was often asked which leadership resources I can recommend, so here is the list of 15 leadership books that had the most influence on me:

𝟭. 𝗛𝗼𝘄 𝗧𝗼 𝗪𝗶𝗻 𝗙𝗿𝗶𝗲𝗻𝗱𝘀 𝗮𝗻𝗱 𝗜𝗻𝗳𝗹𝘂𝗲𝗻𝗰𝗲 𝗣𝗲𝗼𝗽𝗹𝗲

A classic from 1936\. Still very true today. How to advise in communication and influence.

𝟮. 𝟳 𝗛𝗮𝗯𝗶𝘁𝘀 𝗼𝗳 𝗛𝗶𝗴𝗵𝗹𝘆 𝗘𝗳𝗳𝗲𝗰𝘁𝗶𝘃𝗲 𝗣𝗲𝗼𝗽𝗹𝗲

First published in 1990, one of the classics. How to use a principle-centered approach to solve challenges in one's life.

𝟯. 𝗥𝗮𝗱𝗶𝗰𝗮𝗹 𝗖𝗮𝗻𝗱𝗼𝗿

An innovative approach to leadership, how to care personally and challenge directly.

𝟰. 𝗣𝗿𝗶𝗺𝗮𝗹 𝗟𝗲𝗮𝗱𝗲𝗿𝘀𝗵𝗶𝗽

This book employed the concept of emotional intelligence in the business world, which every leader needs.

𝟱. 𝗛𝗶𝗴𝗵 𝗼𝘂𝘁𝗽𝘂𝘁 𝗺𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁

One of my favorite books by Andrew Grove provides a comprehensive overview of a manager's role. 

𝟲. 𝗧𝘂𝗿𝗻 𝘁𝗵𝗮𝘁 𝗦𝗵𝗶𝗽 𝗔𝗿𝗼𝘂𝗻𝗱

A book that talks about great leadership styles applied in a submarine. It explains that everyone can be a leader.

𝟳. 𝗘𝘅𝘁𝗿𝗲𝗺𝗲 𝗢𝘄𝗻𝗲𝗿𝘀𝗵𝗶𝗽

The book explains that you must own everything if you're a leader, no one else you can blame.

𝟴. 𝗟𝗲𝗮𝗱𝗲𝗿𝘀 𝗘𝗮𝘁 𝗟𝗮𝘀𝘁

A famous piece by Simon Sinek, how leaders should sacrifice their own comfort to benefit those who follow them.

𝟵. 𝗖𝗿𝗲𝗮𝘁𝗶𝘃𝗶𝘁𝘆 𝗜𝗻𝗰

A book that describes how building great teams require humility and how we can embrace failure.

𝟭𝟬. 𝗘𝗺𝗼𝘁𝗶𝗼𝗻𝗮𝗹 𝗜𝗻𝘁𝗲𝗹𝗹𝗶𝗴𝗲𝗻𝗰𝗲

A book based on Daniel Goleman's research offers new insights into two minds, rational and emotional.

𝟭𝟭. 𝗧𝗵𝗲 𝗙𝗶𝘃𝗲 𝗗𝘆𝘀𝗳𝘂𝗻𝗰𝘁𝗶𝗼𝗻𝘀 𝗼𝗳 𝗮 𝗧𝗲𝗮𝗺

The books describe five dysfunctions of a team and help leaders avoid failures.

𝟭𝟮. 𝗡𝗼𝗻𝗩𝗶𝗼𝗹𝗲𝗻𝘁 𝗖𝗼𝗺𝗺𝘂𝗻𝗶𝗰𝗮𝘁𝗶𝗼𝗻 

A book describes how we can be compassionate with ourselves and others. 

𝟭𝟯. 𝗧𝗵𝗲 𝗠𝗮𝗸𝗶𝗻𝗴 𝗼𝗳 𝗮 𝗠𝗮𝗻𝗮𝗴𝗲𝗿

It explores what new managers can do in their first three months and beyond to ensure their team gets excellent results.

𝟭𝟰. 𝗗𝗿𝗶𝘃𝗲

The author suggests that great leaders should provide their teams with skills & a sense of purpose.

𝟭𝟱. 𝗚𝗼𝗼𝗱 𝗱𝗼 𝗚𝗿𝗲𝗮𝘁

The book is based on the premise that "good is the enemy of great."

What is your favorite leadership book?

Full list with the links is in the comments.

\_\_\_\_\_\_\_  
If you like my posts please follow me Dr. Milan Milanović and hit the 🔔 on my profile to get a notification for all my new posts.

Grow with me 🚀\!

\#technology \#emotionalintelligence \#business \#leadership \#techworldwithmilan \#books  
…see more

\=== POST 346 \===  
Peter Yang  
View Peter Yang’s profile  
   
• 2nd  
Product Lead at Roblox | Join 100K+ at creatoreconomy.so

3yr •   
3yr Visible to everyone

Microsoft is 48 years old and is arguably the most well-positioned company in big tech for the next decade:

\- Most diversified revenue stream  
\- Azure is clear \#2 in cloud market  
\- In talks to acquire 49% of OpenAI and adding AI to multiple products

Super impressive.  
…see more

\=== POST 347 \===  
Milan Jovanović  
View Milan Jovanović’s profile  
   
• 2nd  
Practical .NET and Software Architecture Tips | Microsoft MVP

3yr •   
3yr Visible to everyone

I spent 3 days optimizing an API endpoint to make it 15x faster.

Here are my secrets.

I faced an issue with an API endpoint for an e-commerce web application that was not scaling well.

The endpoint was responsible for calculating a report and it needed to communicate with multiple modules (services) to gather the necessary data, combine it, and perform the calculations.

I will be breaking down the steps I took to achieve a 15x performance improvement.

The first step I took was to identify the bottlenecks in the system.

When it comes to performance optimization, it's essential to identify the slowest piece of the code, as fixing this will usually give you the most significant improvement. Once you have identified and fixed the first bottleneck, it often reveals the next bottleneck. This is a continuous process and requires constant monitoring and measurement. In my case, the bottlenecks were:  
• Calling the database from a loop  
• Calling an external service multiple times  
• Executing a complex calculation multiple times with identical parameters

Measuring performance is also a crucial step in the optimization process. You can use simple approaches like manually logging execution times between method calls using System.Timers.Timer or use a performance profiler.

The next step I took was to reduce the number of round trips.

A round trip between your application and a database or service can last anywhere between 5-10ms or more. When you have many round trips in your flow, it quickly adds up and causes delays. Here are a few things you can do to reduce the number of round trips:  
• Don't call the database from a loop. Instead, use a simple query like "SELECT \* FROM \[TableName\] WHERE Id IN (list\_of\_ids)"  
• Use a query that returns multiple results sets from the database  
• If you need to make multiple calls to another service, try to convert that into one call and have the service aggregate the required data and return everything at once.

Another step I took was to parallelize external calls.

In my situation, I had multiple asynchronous calls to different services with no dependencies between them. I used the Task.WhenAll method, which allows you to run multiple tasks in parallel. This simple technique helped me achieve significant performance improvement.

Lastly, I considered caching as a last resort after trying all other possibilities to improve performance.

Caching is an effective way to speed up an application, but it can introduce unwanted behavior when the data is stale. When implementing caching, it's important to consider the duration of the cache and the strategies to clear the cache when the underlying data changes. For simple applications, I used the IMemoryCache that is available in ASP .NET Core out of the box, but you can also use an external cache like Redis.

What do you think about my approach? 📝👇  
…see more

\=== POST 348 \===  
Jade Bonacolta  
View Jade Bonacolta’s profile  
   
• 2nd  
Ranked \#1 Female Creator on LinkedIn | Founder of The Quiet Rich™ | Ex-Google | Forthcoming Author | Follow me for daily life hacks

3yr •   
3yr Visible to everyone

Drip your dopamine— don't flood it.

9 daily habits to optimize your brain health, according to experts:

9 daily habits to optimize your brain health

\=== POST 349 \===  
sukhad anand  
View sukhad anand’s profile  
   
• 2nd  
Senior Software Engineer @Google | Techie007 | Opinions and views I post are my own

3yr •   
3yr Visible to everyone

Here are a few recommendations for books that can help you learn about system design in detail:

1\. "Designing Data-Intensive Applications" by Martin Kleppmann is a comprehensive guide to designing, implementing, and maintaining data-intensive applications.

2\. "Building Microservices" by Sam Newman is a book that discusses the principles and practices of building microservices-based systems.

3\. "Systems Performance: Enterprise and the Cloud" by Brendan Gregg is a book that covers performance analysis and optimization for systems running in the cloud.

4\. "Site Reliability Engineering" by Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy is a book that discusses the principles and practices of site reliability engineering, which is a discipline that combines software engineering and systems engineering to build and run large-scale, fault-tolerant systems.

5\. "Designing Distributed Systems" by Brendan Burns is a book that covers the fundamental patterns and practices for designing distributed systems.  
I hope these recommendations are helpful\!

\#engineering \#softwareengineering \#design   
…see more

\=== POST 350 \===  
Christophe Parisel  
View Christophe Parisel’s profile  
   
• 3rd+  
Senior Cloud security architect at Société Générale

3yr •   
3yr Visible to everyone

Sanskrit teachings for computer scientists

Christophe Parisel on LinkedIn • 5+ min read

\=== POST 351 \===  
Hua Li  
View Hua Li’s profile  
   
• 2nd  
FinTech Consulting, Training & Content Strategy｜500k+ Newsletter ｜Founding Member at ByteByteGo｜Executive Director in financial sector｜Director in internet industry

3yr •   
3yr Visible to everyone

How do 𝐁𝐍𝐏𝐋 (Buy Now, Pay Later) providers like Afterpay work?  
How do BNPL providers make money?  
.  
🔹BNPL has grown dramatically in recent years. It rewrites the product payment flow for both eCommerce and POS (Point of Sale) and the BNPL provider is the 𝐩𝐫𝐢𝐦𝐚𝐫𝐲 𝐢𝐧𝐭𝐞𝐫𝐟𝐚𝐜𝐞 between the merchants and the customers.

🔹Benefits for the merchants \- The merchants who offer the BNPL payment option see a 20% increase in cart conversion and a 40% increase in the average order size. 

🔹Benefits for the customers \- The customers can now acquire the product with only the down payment, and pay later with zero interests or fees.

🔹Benefits for BNPL providers \- BNPL providers can sell future installments (receivables) to a lender at a discount. For example, a series of $100 installments to be received in 6 weeks can be sold at $96. This is quite a high interest for the lenders.

The diagram below shows how the process works:

Step 0\. Bob opens an account with AfterPay. This account links to an approved credit/debit card.

Step 1\. Bob wants to buy a $100 product and he chooses the “Buy Now, Pay Later” payment option.

Steps 2-3. BNPL provider checks Bob’s credit score and approves the transaction. 

Steps 4-5. BNPL provider grants Bob a consumer loan of $100, which is usually financed by a bank. $96 out of $100 is paid to the merchant immediately (Yes, the merchant receives less with BNPL than with credit cards\!) Bob now needs to pay back the BNPL provider according to the payment schedule.

Step 6-8. Now Bob pays the BNPL $25 down payment. The payment transaction is sent to Stripe for processing. Stripe forwards it further to the card network. Since this goes through the card network as well, an 𝐢𝐧𝐭𝐞𝐫𝐜𝐡𝐚𝐧𝐠𝐞 𝐟𝐞𝐞 needs to be paid to the card network.

Step 9\. The product is released and can be shipped to Bob.

Steps 10-11. Bob pays installments to the BNPL provider every 2 weeks. The installments are deducted from the credit/debit card and sent to the payment gateway for processing. 

👉 Over to you: Does BNPL benefit the card network? Why?   
—  
👉 If you like my FinTech posts, please follow Hua Li and click the 🔔 on my profile to receive updates.

\#systemdesign \#payments \#fintech \#bnpl   
.  
…see more

\=== POST 352 \===  
Arslan Ahmad  
View Arslan Ahmad’s profile  
   
• 2nd  
Author of Bestselling ‘Grokking’ Series on System Design, Software Architecture & Coding Patterns | Founder DesignGurus.io

3yr •   
3yr Visible to everyone

𝗪𝗵𝗮𝘁 𝗶𝘀 𝗱𝗮𝘁𝗮𝗯𝗮𝘀𝗲 𝘀𝗵𝗮𝗿𝗱𝗶𝗻𝗴?

It is a technique used to scale a database by horizontally partitioning the data across multiple servers, or shards. The goal of sharding is to distribute the data and workload across multiple servers, so that each server can handle a smaller portion of the overall data and workload. This can help improve the performance and scalability of the database, as each server can process queries and updates more efficiently when it is working with a smaller amount of data.

𝗪𝗵𝗮𝘁 𝗮𝗿𝗲 𝘁𝗵𝗲 𝗺𝗼𝘀𝘁 𝗰𝗼𝗺𝗺𝗼𝗻 𝗺𝗲𝘁𝗵𝗼𝗱𝘀 𝗳𝗼𝗿 𝗶𝗺𝗽𝗹𝗲𝗺𝗲𝗻𝘁𝗶𝗻𝗴 𝗱𝗮𝘁𝗮𝗯𝗮𝘀𝗲 𝘀𝗵𝗮𝗿𝗱𝗶𝗻𝗴?

𝗥𝗮𝗻𝗴𝗲-𝗯𝗮𝘀𝗲𝗱 𝘀𝗵𝗮𝗿𝗱𝗶𝗻𝗴: In this approach, the data is partitioned based on a key value, such as a user ID or a timestamp, and the data is distributed across the shards based on the range of the key value. For example, all user IDs in the range of 1-1000 might be stored on one shard, while user IDs in the range of 1001-2000 might be stored on another shard.

𝗛𝗮𝘀𝗵-𝗯𝗮𝘀𝗲𝗱 𝘀𝗵𝗮𝗿𝗱𝗶𝗻𝗴: In this approach, a hash function is used to distribute the data across the shards based on the key value. For example, all data with a user ID of 123 might be stored on one shard, while data with a user ID of 456 might be stored on another shard.

𝗗𝗶𝗿𝗲𝗰𝘁𝗼𝗿𝘆-𝗯𝗮𝘀𝗲𝗱 𝘀𝗵𝗮𝗿𝗱𝗶𝗻𝗴 In this approach, a central directory is used to map the key values to the specific shard where the data is stored. The directory can be used to determine which shard a piece of data belongs to, and the data can be retrieved from the appropriate shard.

𝗖𝘂𝘀𝘁𝗼𝗺 𝘀𝗵𝗮𝗿𝗱𝗶𝗻𝗴: In some cases, it may be necessary to implement a custom sharding strategy that is specific to the needs and requirements of the database and the applications that are using it. This can involve a combination of different sharding methods, or a completely unique approach.

Ref:   
✅ 𝗚𝗿𝗼𝗸𝗸𝗶𝗻𝗴 𝘁𝗵𝗲 𝗦𝘆𝘀𝘁𝗲𝗺 𝗗𝗲𝘀𝗶𝗴𝗻 𝗜𝗻𝘁𝗲𝗿𝘃𝗶𝗲𝘄: https://lnkd.in/g4Wii9r7  
✅ 𝗚𝗿𝗼𝗸𝗸𝗶𝗻𝗴 𝘁𝗵𝗲 𝗔𝗱𝘃𝗮𝗻𝗰𝗲𝗱 𝗦𝘆𝘀𝘁𝗲𝗺 𝗗𝗲𝘀𝗶𝗴𝗻 𝗜𝗻𝘁𝗲𝗿𝘃𝗶𝗲𝘄: https://lnkd.in/dyCRtiec

\#database \#sharding \#systemdesign \#faang \#interview  
…see more

\=== POST 353 \===  
Arslan Ahmad  
View Arslan Ahmad’s profile  
   
• 2nd  
Author of Bestselling ‘Grokking’ Series on System Design, Software Architecture & Coding Patterns | Founder DesignGurus.io

3yr •   
3yr Visible to everyone

𝗦𝘆𝘀𝘁𝗲𝗺 𝗗𝗲𝘀𝗶𝗴𝗻 𝗕𝗮𝘀𝗶𝗰𝘀: 𝗗𝗶𝗳𝗳𝗲𝗿𝗲𝗻𝗰𝗲 𝗯𝗲𝘁𝘄𝗲𝗲𝗻 𝗮𝗻 𝗔𝗣𝗜 𝗚𝗮𝘁𝗲𝘄𝗮𝘆 𝗮𝗻𝗱 𝗮 𝗟𝗼𝗮𝗱 𝗕𝗮𝗹𝗮𝗻𝗰𝗲𝗿

An API gateway is focused on 𝗿𝗼𝘂𝘁𝗶𝗻𝗴 requests to the appropriate microservice, while a load balancer is focused on 𝗱𝗶𝘀𝘁𝗿𝗶𝗯𝘂𝘁𝗶𝗻𝗴 requests evenly across a group of backend servers.

An API gateway and a load balancer are both types of infrastructure that can be used in a computer network to manage incoming requests and enhance the performance of a system. However, they work in different ways and serve different purposes.

𝗔𝗣𝗜 𝗴𝗮𝘁𝗲𝘄𝗮𝘆: An API gateway is a type of middleware that sits between a client and a collection of microservices. Its main purpose is to route requests from clients to the appropriate microservice and then to return the response from the microservice back to the client. An API gateway can also perform other tasks such as authorization, rate limiting, and caching.

𝗟𝗼𝗮𝗱 𝗯𝗮𝗹𝗮𝗻𝗰𝗲𝗿: A load balancer, on the other hand, is a type of infrastructure that distributes incoming requests evenly across a group of backend servers in order to improve the performance and availability of a system. Load balancers are typically used to handle requests that are sent to a single, well-known IP address, and then route them to one of many possible backend servers based on factors such as server performance and availability.

Another difference between the two is the type of requests that they typically handle. An API gateway is typically used to handle requests for APIs, which are web-based interfaces that allow applications to interact with each other over the internet. These requests typically have a specific URL that identifies the API that the client is trying to access, and the API gateway routes the request to the appropriate microservice based on this URL. A load balancer, on the other hand, is typically used to handle requests that are sent to a single, well-known IP address, and then routes them to one of many possible backend servers based on factors such as server performance and availability.

\#microservices \#api \#apigateway \#loadbalancer \#systemdesign   
…see more

\=== POST 354 \===  
Sidharth Kriplani  
View Sidharth Kriplani’s profile  
   
• 2nd  
Senior Data Analyst at Uber

3yr •   
3yr Visible to everyone

You want to reach an intermediate SQL level inside a week❓

💯 I have the recipe for it 

Yeah, no kidding. Seriously

\<35 questions (without counting SQL Bolt, which is a simple 1 hour task really) and you will confidently be able to face SQL questions shot at you in an interview

As I had promised in my last post (bit.ly/3X0LPfc), here is the first "SQL preparation kit" that is custom made for the following purposes:

\-- only for facing SQL questions in interviews  
\-- can be covered in \< week  
\-- can take a complete beginner to intermediate level   
\-- you can use this kit if you are already good at SQL but need a quick and serious warmup before your important interview 

Pre \- requisites?   
\-- none. If you know some SQL before, cool. If you know some other programming language already, awesome. If you can google, best

Here it goes:

Day One:  
SQL Bolt (sqlbolt.com)  
Data Science Skills (bit.ly/3i6obPg) (EASY)

Day Two:  
Average Post Hiatus (bit.ly/3WRPv2I) (EASY)  
Teams Power Users (bit.ly/3jCIggI) (EASY)  
Cards Issued Difference (bit.ly/3YUdhgi) (EASY)  
Pharmacy Analytics Part 1 (bit.ly/3hWwb5q) (EASY)  
Pharmacy Analytics Part 2 (bit.ly/3Q2Gm53) (EASY)  
Most Expensive Purchase (bit.ly/3VrvIWx) (EASY) (Premium)

Day Three:  
Unfinished Parts (bit.ly/3Vydpzd) (EASY)  
Compressed Mean (bit.ly/3C8oDUf) (EASY)  
ApplePay Volume (bit.ly/3Cb9Sjg) (EASY) (Premium)  
Subject Matter Experts (bit.ly/3Grfskj) (EASY) (Premium)  
Highest Number of Products (bit.ly/3Go3LL0) (EASY) (Premium)  
Ad Campaign ROAS (bit.ly/3i0bNAw) (EASY) (Premium)  
Top Rated Businesses (bit.ly/3hSqjdG) (EASY) (Premium)

Day Four:  
Average Deal Size (Part 2\) (bit.ly/3vpRj7k) (MEDIUM) (Premium)  
Email Table Transformation (bit.ly/3WSr2Kq) (MEDIUM) (Premium)  
LinkedIn Power Creators (Part 2\) (bit.ly/3FZf8aR) (MEDIUM) (Premium)  
Advertiser Status (bit.ly/3i2mhzh) (HARD)  
Average Vacant Days (bit.ly/3Wun3nC) (HARD) (Premium)  
3-Topping Pizzas (bit.ly/3GpHxIA) (HARD)  
Bad Delivery Rate (bit.ly/3IeNmKt) (HARD) (Premium)

Day Five:  
Fill Missing Client Data (bit.ly/3C8JaYu) (MEDIUM)  
First Transaction (bit.ly/3vmsmJW) (MEDIUM) (Premium)  
Google Maps Flagged UGC (bit.ly/3IdKrS3) (MEDIUM) (Premium)  
Event Friends Recommendation (bit.ly/3jCzyiz) (HARD) (Premium)  
Follow-Up Airpod Percentage (bit.ly/3G562tl) (HARD) (Premium)

Day Six:  
Highest-Grossing Items (bit.ly/3jE697G) (MEDIUM)  
Best-Selling\_Product (bit.ly/3GnytnF) (MEDIUM)  
International Call Percentage (bit.ly/3PXrNzO) (MEDIUM)  
Reactivated Users (bit.ly/3GqWzhh) (HARD) (Premium)

Day Seven:  
Tweet's Rolling Averages (bit.ly/3I9JuKn) (MEDIUM)  
Rolling 3-Day Earnings (bit.ly/3vHPral) (HARD) (Bonus)

Note: some of the problems are "premium" problems 

\#interview \#data \#job \#sql  
…see more

\=== POST 355 \===  
Sumit Mittal  
View Sumit Mittal’s profile  
   
• 2nd  
Founder @ TrendyTech.in | Data Engineering & GenAI Mentor | 400K+ Followers | Shaping the Next Generation of Data Engineers

3yr •   
3yr Visible to everyone

Excellent demonstration of end to end Data Engineering Pipeline

Data Sources \- There are multiple sources of data.   
Structured, Unstructured, Semistructured.

Data Loaders \- All this data is then ingested to the Data Lake.

Once the Data is in Data Lake, we keep doing multiple transformations and the data quality keeps getting better at each stage.

The cleaned up / processed data is then given to various visualization tools to get insights from it.

This is a perfect ELT pipeline (Extract Load Transform). Here we load everything first in the Data Lake and then later we transform the data to seek for insights.

Image Credit : Semantix

\#dataengineering \#visualization \#quality \#bigdata \#ml \#datascience \#sumitteaches \#dataanalytics \#datalake   
…see more

\=== POST 356 \===  
Status is online  
Nimit Aggarwal  
View Nimit Aggarwal’s profile  
   
• 2nd  
Engineering @Instagram | 10k+ follower | Ex-Directi, BrowserStack | Backend | Node.js | GraphQL | ReactJS

3yr •   
3yr Visible to everyone

Hey folks\! I had some time in my hand before the new year, so decided to make a new portfolio website. Here it is hosted at https://nimitaggarwal.me 🎉🎉🎉.

The code is open-sourced at https://lnkd.in/dnUnBEEj. The website is built with Next.js and hosted on Vercel.

Feel free to browse through the website and post any feedback in the comments. 

\#javascript \#softwareengineering \#react \#code \#programming \#css \#webdevelopment \#nextjs \#vercel \#meta \#indian \#instagram 

…see more

Nimit Aggarwal | Software Engineer @Meta

nimitaggarwal.me

\=== POST 357 \===  
Milan Jovanović  
View Milan Jovanović’s profile  
   
• 2nd  
Practical .NET and Software Architecture Tips | Microsoft MVP

3yr •   
3yr Visible to everyone

What is the Outbox pattern? 📦📦📦

The Outbox pattern is a way of implementing event-driven architectures in a more reliable and consistent way.

It involves the use of an "outbox" table in a database, which acts as a buffer for outgoing events. When an event is triggered, it is added to the outbox table and then later processed and emitted to the appropriate event handlers.

One of the main benefits of the Outbox pattern is that it provides a way to decouple the source of an event from the event handlers.

This makes it easier to scale and maintain the system, as the event handlers can be updated or replaced without affecting the source of the events.

Additionally, the outbox table acts as a buffer for events, ensuring that they are not lost if the event handlers are temporarily unavailable.

Another benefit of the Outbox pattern is that it allows for better transactionality and atomicity. Since events are stored in the outbox table before being processed, it is easy to roll back events if there is a problem with the transaction. This can be especially useful in cases where events need to be emitted in a specific order or where there are dependencies between events.

There are also some potential downsides to the Outbox pattern.

One potential issue is that the outbox table can become large over time, especially in systems with a high volume of events. This can lead to performance issues and may require periodic cleanup or maintenance.

Additionally, the Outbox pattern can add complexity to the system, as it requires the use of an additional database table and the implementation of event processing logic.

While it does add some complexity to the system, the benefits of improved decoupling, transactional support, and event reliability can make it worth the effort.

It is important to carefully consider the trade-offs and determine whether the Outbox pattern is a good fit for a given system.

Did you ever implement the Outbox pattern on a project? 📝👇

\#softwareengineering \#dotnet \#outbox   
…see more

\=== POST 358 \===  
Rocky Bhatia  
View Rocky Bhatia’s profile  
   
• 2nd  
400K+ Engineers | Architect @ Adobe | GenAI & Systems at Scale

3yr •   
3yr Visible to everyone

How to Become a Software Architect 

Being a good architect is achieved by applying and implementing more than reading.

After getting 100's DM on the guidance of becoming a software architect, Based on my working experience, I have created the below roadmap.

The position of a software architect requires a profound knowledge of software functionality, performance, viability, scalability, comprehensibility, security, and technological constraints.

Language :

To start your career as a Software Architect, you should have a sound knowledge of programming languages & frameworks.  
Architects lead the team of developers, collaborate with other groups, review code, etc. hence one must have a thorough understanding of programming concepts and paradigms.

Architecture Pattern and Style :

In software engineering, a design pattern is a general, reusable solution for solving a common problem when designing an application or system.

Microservice  
Event Driven  
Layered   
Master-Slave  
Publisher Subscriber 

Design Principal and Pattern 

A design pattern is more of a template to approach the problem.

Design Pattern \- GOF , OOPS principle, programming Paradigms.   
ACID (Atomicity, Consistency, Isolation, Durability)   
CAP (Consistency, Availability, Partition Tolerance)   
SOLID   
Domain-driven design 

Important Skills :  
An architect takes all Technology, Architecture, and Design Decisions and conducts the POT and POC.  
He mentors technical teams and promotes quality standards and the right vision of the product. As a result, they should be able to win authority and respect.  
An architect communicates with stakeholders, business analysts, and engineers, explaining the benefits of employing certain technologies or applying a specific pattern. He manages the system design and should be able to identify risks timely. 

Operational Knowledge \- one should have working experience in some of the following areas to make a better decision. 

Containers   
IAAS .  
Serverless   
CI/CD .  
Cloud design   
Distributed computing   
LB   
Security Gateway 

Data and Analytics: One should have strong hands with the some of the following tools 

SQL and NoSQL databases   
Batch processing ( Spark ,Hadoop)  
Stream Processing ( flink, spark streaming ,storm)  
Warehouse (hive, snowflake )

Tools \- Hands on experience with Important tools like   
git, maven,check style,find bugs,   
Jira, sonar, jenkins,   
JMeter ,splunk etc 

API and Integration \- Rest/Soap/graphql and api management like mule soft, messaging queues . 

Security \- Security aspects related to Certificate ,credential data at rest ,data in motion 

Architects can further be divided into the following categories(Future Post) :  
Enterprise /Solution /Cloud Architect/Big Data Architect 

I will plan to cover each component and each technical area in details in future posts .

\#software \#distributedcomputing \#security \#nosql \#programming \#career \#sql \#softwarearchitecture \#data \#softwareengineering \#cloud \#technology \#bigdata 

…see more

\=== POST 359 \===  
Milan Jovanović  
View Milan Jovanović’s profile  
   
• 2nd  
Practical .NET and Software Architecture Tips | Microsoft MVP

3yr •   
3yr Visible to everyone

Can you learn to embrace eventual consistency? ⏳

I've had the opportunity to work on a variety of architectures, including event-driven ones.

One concept that has always been important in these systems is eventual consistency.

For those unfamiliar with the term, eventual consistency refers to the idea that, in a distributed system, data changes may not be immediately reflected across all nodes.

This can happen for a variety of reasons \- for example, network delays or temporary failures.

In event-driven architectures, this concept is especially important because events are often used to trigger actions or updates in the system.  
If the system is not eventually consistent, it could lead to issues such as data discrepancies or unexpected behavior.

To illustrate the importance of eventual consistency, let me share a story from one of my past projects.

We were building an event-driven system for a large e-commerce company.

The system was designed to automatically update inventory levels whenever an order was placed or canceled.

At first, everything seemed to be working as expected.

But as the system scaled and more orders started flowing through, we started to notice strange behavior.  
Sometimes, inventory levels would be incorrect \- for example, we might have more items in stock than we should have or vice versa.

After some investigation, we realized that the issue was due to eventual consistency.

Because our system was distributed and events were being processed asynchronously, there was a chance that an order event might not be processed immediately.

This meant that the inventory update might not happen until some time later, leading to the discrepancies we were seeing.

To fix the issue, we had to redesign the system to take eventual consistency into account.

We added retry logic to ensure that events were eventually processed, and we also implemented conflict resolution strategies to ensure that the system eventually converged on the correct inventory levels.

It was a challenging process, but in the end, we were able to build a much more robust and scalable system.

And it was all thanks to the understanding and designing for eventual consistency.

In my experience, eventual consistency can be a challenging concept to wrap your head around at first.

But once you understand it and know how to design for it, it becomes an essential part of building robust, scalable event-driven systems.

So if you're working on an event-driven architecture, be sure to keep eventual consistency in mind \- it could save you a lot of headaches down the road.

Did you work with an event-driven architecture before? 📝👇

\#softwareengineering \#softwarearchitecture \#dotnet \#eventdrivenarchitecture   
…see more

\=== POST 360 \===  
Manu Agrawal  
View Manu Agrawal’s profile  
   
• 2nd  
Senior Software Engineer | Agentic AI & Gen-AI | Full Stack Engineer | Joshtalks Speaker | Featured on 10+ News channels | Ex Google

3yr •   
3yr Visible to everyone

Follow these Links to Learn design Patterns

Best Github Article   
https://lnkd.in/dfNiqcBx

Learn Language wise design Patterns  
https://lnkd.in/dT86MKHE

Design Patterns in 5 Mins  
https://lnkd.in/dtFBzVC4

My Personal Favourite \- In Depth Design Pattern Playlist   
https://lnkd.in/d36y4\_pz

10 Design Patterns in 10 Mins  
https://lnkd.in/dP7k7BcN

Do Follow Manu Agrawal for more such content.

\#design \#github \#language \#designpatterns \#java \#designpattern   
…see more

\=== POST 361 \===  
Status is reachable  
Tannishk Sharma  
View Tannishk Sharma’s profile  
   
• 1st  
Senior AI Product Manager | Amazon | Scaled E-commerce Products to 50M+ Users | 100 M+ Cost Savings | Fintech | Payments | Ex-Paytm, Urban company , Udaan

3yr •   
3yr Visible to everyone

If you are stuck on a problem, don't sit there and think about it. Just start working on it. Even if you don't know what you are doing, the simple act of working on it will eventually cause the right ideas to show up in your head.

\- Mark Manson

\#problemsolving \#implementation   
…see more

\=== POST 362 \===  
Brij kishore Pandey  
View Brij kishore Pandey’s profile  
   
• 2nd  
AI Architect & Engineer | AI Strategist

3yr •   
3yr Visible to everyone

🚀 Master 9 HTTP methods in just 9 minutes and stand out in 2023\!

🔸 As a developer, it's always important to stay up-to-date with the latest technologies and skills. 

🔸 While it may seem like knowing just 4-5 REST API HTTP methods is enough, the reality is that there are actually 39 different verbs or methods available. 

🌀 However, if you want to set yourself apart in the job market in 2023, it's crucial to master at least 9 of these methods.

👉 The GET Method allows you to retrieve data from a server.   
👉 The POST Method allows you to send data to a server to create a resource.   
👉 The PUT Method allows you to update a resource on a server.   
👉 The PATCH Method allows you to update a resource on a server using partial data.   
👉 The DELETE Method allows you to delete a resource on a server.   
👉 The HEAD Method allows you to retrieve metadata from a server.   
👉 The OPTIONS Method allows you to describe the communication options for a resource.   
👉 The TRACE Method allows you to trace the communication path between a client and a server.   
👉 The CONNECT Method allows you to establish a tunnel to a server.

✔️ Knowing these 9 methods can give you a significant advantage in the job market, as they are essential for building powerful and efficient REST APIs. 

📍 And if you want to learn more about these methods in just 9 minutes, be sure to check out the attached PDF. 

📞 I have created a Telegram channel for sharing knowledge and have included the link in the comments section.

🙏 If you like my posts, please follow Brij Kishore Pandey 🇺🇸 🌐🌐 and hit the 🔔 on my profile to get a notification for all my new posts.

\#data \#developer \#job \#communication \#softwaredevelopment \#softwareengineering \#building   
…see more

9 HTTP Methods

\=== POST 363 \===  
Adil Adilli  
View Adil Adilli’s profile  
   
• 2nd  
Lead AI Software Engineer | Ex-Google

3yr •   
3yr Visible to everyone

📚 Top 10 Greatest Software Development Books of All Time 📚   
   
📘 There are many ways that one can acquire knowledge. Some read books, some learn by code reviews and discussions, some through coursework. To facilitate faster growth, I’m firmly convinced that every software developer needs to read at least a few books.  
   
📕 Based on my own experience, as well as similar lists gathered from other sources and the experience of many colleagues, I compiled a list that every software developer should read.   
   
📗 These books are language agnostic and the knowledge can be transferred to all other languages.

1️⃣ Clean Code by Robert C. Martin  
https://lnkd.in/g5n9iPkd

2️⃣ Design Patterns by Elements of Reusable Object-Oriented Software  
by Erich Gamma, Richard Helm, Ralph Johnson and John Vlissides  
https://lnkd.in/gWppumsj

3️⃣ Introduction to Algorithms Thomas Cormen, Charles Leiserson, Ronald Rivest, Clifford Stein  
https://lnkd.in/d32pyYQp

4️⃣ The Pragmatic Programmer by David Thomas and Andrew Hunt  
https://lnkd.in/gxXHAfA7

5️⃣ Designing Data-Intensive Applications, Martin Kleppmann  
https://lnkd.in/gjYvjBWt

6️⃣ Code Complete by Steve McConell  
https://lnkd.in/gZDCQy8q

7️⃣ Working Effectively with Legacy Code by Michael C. Feathers  
https://lnkd.in/gvuY2ZP2

8️⃣ Refactoring: Improving the Design of Existing Code by Martin Fowler  
https://lnkd.in/gqAk2FaU

9️⃣ Soft Skills: The software developer's life manual,John Sonmez  
https://lnkd.in/gjMHEG2G

🔟 Patterns of Enterprise Application Architecture by Martin Fowler  
https://lnkd.in/gXBT7eTW

❓ What do you think which book would you love to have in this list? Any book that has helped you to learn and grow that deserves a mention❓

\#softwareengineering \#programming \#books \#personaldevelopment \#careerintech \#careerguide \#cleancode \#algorithms 

…see more

\=== POST 364 \===  
Hussein Nasser  
View Hussein Nasser’s profile  
   
• 3rd+  
Software Engineer | Talks about backend, databases and operating systems

3yr •   
3yr Visible to everyone

RabbitMQ streams feature was introduced last year, offering a way to read messages and keep them as opposed to queues which pops messages. This is effectively very similar if not identical to Kafka’s. 

The only difference it seems Kafka clients uses long polling while RMQ Push  
…see more

\=== POST 365 \===  
Mark O'Neill  
View Mark O'Neill’s profile  
   
• 3rd+  
VP Distinguished Analyst and Chief of Research

3yr •   
3yr Visible to everyone

My Top Three Software Engineering Books of 2022

Like many Gartner analysts, the background for my video calls is a set of bookshelves. It's less exciting than other analysts backgrounds: like Jim Scheibmeir, Ph.D. with his wall of guitars, Jason Wong with his ever-changing travel photos, or indeed Peter Hyde who has a lot more books than I do. But it's handy for me to reach back and pick up a useful book \- something I've often been known to do with Team Topologies or Software Engineering at Google. 2022 has been a great year for adding new books, and here are my three favorite books published this year: 

The Staff Engineer's Path by Tanya Reilly. 

This book is timely because in our software engineering research at Gartner this year, we've seen architect roles being replaced by Principle or Staff Engineer roles. My colleagues Dave Micko and Tigran Egiazarov have noted that architecture then becomes an emergent quality of the ecosystem, rather than a directed, top-down imperative. Of course, Staff Engineers are concerned with more than architecture, and this book fully captures the broad role of the staff engineer. It explains where they fit in an engineering organization, and also includes many practical tips for engineers considering moving into this position. I loved how this book ties in other important concepts such as Domain-Driven Design and Nemawashi (I also didn't know this term before\!). Highly recommended. 

Observability Engineering by Charity Majors, Liz Fong-Jones, and George Miranda

Observability has been everywhere in 2022, and we expect it to also be a major trend in 2023\. In fact, Applied Observability is one of our Gartner Top Strategic Trends for 2023\. So this book is very welcome. It does a great job of addressing the question "Is this just the new name for monitoring?". I imagine the authors must get this question a lot (we certainly do at Gartner) and they take the time to explain what is novel and valuable about observability engineering. Although the authors work for a vendor (Honeycomb), they cover alternatives, including open source, also. I especially appreciated the code examples, written in Go, covering many OpenTelemetry concepts and scenarios. 

Engineering Management for the Rest of Us by Sarah Drasner. 

This is the book I recommend to anyone moving into an EM (engineering manager) position. It does a fantastic job of covering the delta over and above technical chops which are required of an EM. It is full of practical advice, such as how to run 1:1's with your team, how to consider technical debt, how to deal with conflict, and how to manage your time. The section on "How to say no" is worth the book's price in itself. I loved all the real-life examples that Sarah Drasner included from her own experience. e.g. the fact that in Google, they use a Chrome extension to track the amount of time you're spending talking in meetings. 

I highly recommend these books as gifts or as holiday downtime reading\!  
…see more

\=== POST 366 \===  
Status is online  
Ron Fybish  
View Ron Fybish’s profile  
   
• 2nd  
Co-Founder @ Foundera.co | Turning Founders into Thought Leaders on LinkedIn

3yr •   
3yr Visible to everyone

How are Passwords Stored? 🔐 🆘 

do you want to know how to keep user passwords safe?

The primary security mechanism when storing passwords. 𝙄𝙩 𝙞𝙨 𝙣𝙤𝙩 \- 𝙀𝙣𝙘𝙧𝙮𝙥𝙩𝙞𝙤𝙣, 𝘽𝙪𝙩 𝙧𝙖𝙩𝙝𝙚𝙧 \- 𝙃𝙖𝙨𝙝𝙞𝙣𝙜.

🔑 𝗘𝗻𝗰𝗿𝘆𝗽𝘁𝗶𝗼𝗻  
Encrypting a text means that it is possible to get the text back by decrypting it. An authorized person can know the user's password by decrypting it if they know the key.

🔑 𝗛𝗮𝘀𝗵𝗶𝗻𝗴  
Hashing is a way to encrypt text. When we hash something, it produces a digest. But you cannot decrypt the text from the digest.

🔑 𝗬𝗼𝘂 𝗰𝗮𝗻 𝗮𝗹𝘀𝗼 𝗦𝗮𝗹𝘁 𝘁𝗵𝗲 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱  
Salt is a unique piece of data for each user and is added to the \#password before it is hashed. This will also ensure that no two passwords have the same hash.

🅻🅸🅱🆁🅰🆁🅸🅴🆂 📚   
The most popular password-hashing algorithms are: 𝗕𝗖𝗥𝗬𝗣𝗧, 𝗣𝗕𝗞𝗗𝗙𝟮

👉 𝘜𝘴𝘪𝘯𝘨 𝘢 𝘭𝘪𝘣𝘳𝘢𝘳𝘺 𝘧𝘰𝘳 𝘩𝘢𝘴𝘩𝘪𝘯𝘨 𝘱𝘢𝘴𝘴𝘸𝘰𝘳𝘥𝘴 𝘪𝘴 𝘢𝘭𝘸𝘢𝘺𝘴 𝘳𝘦𝘤𝘰𝘮𝘮𝘦𝘯𝘥𝘦𝘥 𝘪𝘯𝘴𝘵𝘦𝘢𝘥 𝘰𝘧 𝘵𝘳𝘺𝘪𝘯𝘨 𝘵𝘰 𝘪𝘮𝘱𝘭𝘦𝘮𝘦𝘯𝘵 𝘺𝘰𝘶𝘳 𝘰𝘸𝘯. \#security   
…see more

How are Passwords Stored?

\=== POST 367 \===  
Ankit Pangasa  
View Ankit Pangasa’s profile  
   
• 2nd  
Engineering Manager at Adobe | Ex-Google | Breaking down interviews, system design & career growth | Sharing only verified job opportunities | Opinions my own | DM for collab

3yr •   
3yr Visible to group only

🚀 Often we as Engineers are so involved in preparing for tech questions that we completely ignore the non-tech portion of interviews.👹

🚀 Every now and then you would be asked questions like:  
 💎 why are you looking for a change?  
 💎 are you a team player?  
 💎 what is one thing you want to change in yourself?  
 💎 and many more...

🚀 What you should definitely not do is fake answers for such questions. Because once the interviewer goes deep in any of the question, you would be in trouble. 🤯

🚀 But you should definitely prepare answers for these questions based on your experience and aspirations. 🤠

🚀 Sharing a list of such questions which you should definitely prepare before going for \#interview. 🛸

👀 Follow Ankit Pangasa. 👐 And do like, share, comment and save this document. 👍❤️⏺️

\#software \#linux \#networking \#security \#content \#windows \#email \#like \#share \#learning \#unix \#utilities \#comment \#python \#share \#like \#comment \#datascientist \#data \#coding \#programming \#datastructuresandalgorithms \#java \#tech \#softwaretesting \#softwaredevelopment \#programming \#python \#learning \#content \#quickread \#quickbooks \#data \#datastructures \#competitiveprogramming \#oopsconcepts \#oops \#designpatterns \#springframework \#spring \#microsoft \#amazon \#apple \#facebook \#cisco \#vmware \#xerox \#startups \#softwareengineering \#developer \#engineering \#engineer \#networking \#careers \#startups \#socialmedia \#linkedin \#linkedinposts \#technology \#like \#share \#reference \#complexity \#classes \#objects \#design \#comment \#scaler \#scalerdiscord \#scalerlearning \#scaleracademy \#internet \#protocol \#c \#cpp \#cplusplusdeveloper \#cplusplus \#cprogramming \#cdeveloper \#docker \#devops \#datastructures \#interviewpreparation \#interview \#interviewtips   
…see more

ntq

\=== POST 368 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗪𝗵𝗮𝘁 𝗶𝘀 𝘁𝗵𝗲 𝗧𝘄𝗲𝗹𝘃𝗲-𝗙𝗮𝗰𝘁𝗼𝗿 𝗔𝗽𝗽 ?

It describes many well-tested architectural patterns and best practices for use with 𝘀𝗼𝗳𝘁𝘄𝗮𝗿𝗲-𝗮𝘀-𝗮-𝘀𝗲𝗿𝘃𝗶𝗰𝗲 (𝗦𝗮𝗮𝗦) 𝗮𝗽𝗽𝗹𝗶𝗰𝗮𝘁𝗶𝗼𝗻𝘀. When apps are deployed to the web, they can be created with portability and resilience thanks to these best practices. 

The Twelve Factors:

𝗜. 𝗖𝗼𝗱𝗲𝗯𝗮𝘀𝗲  
One codebase tracked in revision control, many deploys

𝗜𝗜. 𝗗𝗲𝗽𝗲𝗻𝗱𝗲𝗻𝗰𝗶𝗲𝘀  
Explicitly declare and isolate dependencies

𝗜𝗜𝗜. 𝗖𝗼𝗻𝗳𝗶𝗴  
Store config in the environment

𝗜𝗩. 𝗕𝗮𝗰𝗸𝗶𝗻𝗴 𝘀𝗲𝗿𝘃𝗶𝗰𝗲𝘀  
Treat backing services as attached resources

𝗩. 𝗕𝘂𝗶𝗹𝗱, 𝗿𝗲𝗹𝗲𝗮𝘀𝗲, 𝗿𝘂𝗻  
Strictly separate build and run stages

𝗩𝗜. 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗲𝘀  
Execute the app as one or more stateless processes

𝗩𝗜𝗜. 𝗣𝗼𝗿𝘁 𝗯𝗶𝗻𝗱𝗶𝗻𝗴  
Export services via port binding

𝗩𝗜𝗜𝗜. 𝗖𝗼𝗻𝗰𝘂𝗿𝗿𝗲𝗻𝗰𝘆  
Scale out via the process model

𝗜𝗫. 𝗗𝗶𝘀𝗽𝗼𝘀𝗮𝗯𝗶𝗹𝗶𝘁𝘆  
Maximize robustness with fast startup and graceful shutdown

𝗫. 𝗗𝗲𝘃/𝗽𝗿𝗼𝗱 𝗽𝗮𝗿𝗶𝘁𝘆  
Keep development, staging, and production as similar as possible

𝗫𝗜. 𝗟𝗼𝗴𝘀  
Treat logs as event streams

𝗫𝗜𝗜. 𝗔𝗱𝗺𝗶𝗻 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗲𝘀  
Run admin/management tasks as one-off processes

Check the links in the comments.

Image credits: Net solutions.

\_\_\_\_\_\_\_  
If you like my posts please follow me Dr. Milan Milanović and hit the 🔔 on my profile to get a notification for all my new posts.

Grow with me 🚀\!

\#technology \#softwareengineering \#programming \#cloudcomputing \#techworldwithmilan  
…see more

\=== POST 369 \===  
Vitto Rivabella  
View Vitto Rivabella’s profile  
   
• 3rd+  
AI at Ethereum Foundation | Ex. Head of product Cyfrin | Ex. Lead DevRel Alchemy | Web3 & Blockchain Developer | Speaker | Helping devs break into web3

3yr •   
3yr Visible to everyone

7 YouTube channels I love \- for Web3 developers:

1\) Patrick Collins  
2\) Nader Dabit  
3\) Alchemy Platform  
4\) HashLips NFT  
5\) Alchemy University  
6\) Smart contract programmer  
7\) Josh's DevBox  
…see more

\=== POST 370 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗦𝗼𝗳𝘁𝘄𝗮𝗿𝗲 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲 𝗕𝗼𝗼𝗸𝘀𝗵𝗲𝗹𝗳

Which books are on your software architecture bookshelf ?

𝟭. 𝗝𝘂𝘀𝘁 𝗘𝗻𝗼𝘂𝗴𝗵 𝗦𝗼𝗳𝘁𝘄𝗮𝗿𝗲 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲: 𝗔 𝗥𝗶𝘀𝗸-𝗗𝗿𝗶𝘃𝗲𝗻 𝗔𝗽𝗽𝗿𝗼𝗮𝗰𝗵

𝟮. 𝗥𝗲𝗹𝗲𝗮𝘀𝗲 𝗜𝘁\!: 𝗗𝗲𝘀𝗶𝗴𝗻 𝗮𝗻𝗱 𝗗𝗲𝗽𝗹𝗼𝘆 𝗣𝗿𝗼𝗱𝘂𝗰𝘁𝗶𝗼𝗻-𝗥𝗲𝗮𝗱𝘆 𝗦𝗼𝗳𝘁𝘄𝗮𝗿𝗲 

𝟯. 𝗖𝗼𝗻𝘁𝗶𝗻𝘂𝗼𝘂𝘀 𝗗𝗲𝗹𝗶𝘃𝗲𝗿𝘆: 𝗥𝗲𝗹𝗶𝗮𝗯𝗹𝗲 𝗦𝗼𝗳𝘁𝘄𝗮𝗿𝗲 𝗥𝗲𝗹𝗲𝗮𝘀𝗲𝘀 𝘁𝗵𝗿𝗼𝘂𝗴𝗵 𝗕𝘂𝗶𝗹𝗱, 𝗧𝗲𝘀𝘁, 𝗮𝗻𝗱 𝗗𝗲𝗽𝗹𝗼𝘆𝗺𝗲𝗻𝘁 𝗔𝘂𝘁𝗼𝗺𝗮𝘁𝗶𝗼𝗻

𝟰. 𝗕𝘂𝗶𝗹𝗱𝗶𝗻𝗴 𝗠𝗶𝗰𝗿𝗼𝘀𝗲𝗿𝘃𝗶𝗰𝗲𝘀: 𝗗𝗲𝘀𝗶𝗴𝗻𝗶𝗻𝗴 𝗙𝗶𝗻𝗲-𝗚𝗿𝗮𝗶𝗻𝗲𝗱 𝗦𝘆𝘀𝘁𝗲𝗺𝘀

𝟱. 𝗔𝗴𝗶𝗹𝗲 𝗦𝘆𝘀𝘁𝗲𝗺𝘀 𝗘𝗻𝗴𝗶𝗻𝗲𝗲𝗿𝗶𝗻𝗴

𝟲. 𝗦𝗼𝗳𝘁𝘄𝗮𝗿𝗲 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲 𝗳𝗼𝗿 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿𝘀

𝟳. 𝗦𝗼𝗳𝘁𝘄𝗮𝗿𝗲 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲 𝗶𝗻 𝗣𝗿𝗮𝗰𝘁𝗶𝗰𝗲

𝟴. 𝗧𝗵𝗲 𝗦𝗼𝗳𝘁𝘄𝗮𝗿𝗲 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁 𝗘𝗹𝗲𝘃𝗮𝘁𝗼𝗿: 𝗥𝗲𝗱𝗲𝗳𝗶𝗻𝗶𝗻𝗴 𝘁𝗵𝗲 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁'𝘀 𝗥𝗼𝗹𝗲 𝗶𝗻 𝘁𝗵𝗲 𝗗𝗶𝗴𝗶𝘁𝗮𝗹 𝗘𝗻𝘁𝗲𝗿𝗽𝗿𝗶𝘀𝗲

𝟵. 𝗙𝘂𝗻𝗱𝗮𝗺𝗲𝗻𝘁𝗮𝗹𝘀 𝗼𝗳 𝗦𝗼𝗳𝘁𝘄𝗮𝗿𝗲 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲

𝟭𝟬. 𝗗𝗶𝘀𝘁𝗿𝗶𝗯𝘂𝘁𝗲𝗱 𝗦𝘆𝘀𝘁𝗲𝗺𝘀

𝟭𝟭. 𝗗𝗼𝗺𝗮𝗶𝗻-𝗗𝗿𝗶𝘃𝗲𝗻 𝗗𝗲𝘀𝗶𝗴𝗻: 𝗧𝗮𝗰𝗸𝗹𝗶𝗻𝗴 𝗖𝗼𝗺𝗽𝗹𝗲𝘅𝗶𝘁𝘆 𝗶𝗻 𝘁𝗵𝗲 𝗛𝗲𝗮𝗿𝘁 𝗼𝗳 𝗦𝗼𝗳𝘁𝘄𝗮𝗿𝗲

𝟭𝟮. 𝗦𝗼𝗳𝘁𝘄𝗮𝗿𝗲 𝗦𝘆𝘀𝘁𝗲𝗺𝘀 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲: 𝗪𝗼𝗿𝗸𝗶𝗻𝗴 𝘄𝗶𝘁𝗵 𝗦𝘁𝗮𝗸𝗲𝗵𝗼𝗹𝗱𝗲𝗿𝘀 𝗨𝘀𝗶𝗻𝗴 𝗩𝗶𝗲𝘄𝗽𝗼𝗶𝗻𝘁𝘀 𝗮𝗻𝗱 𝗣𝗲𝗿𝘀𝗽𝗲𝗰𝘁𝗶𝘃𝗲𝘀

Bonus: 𝗖𝗹𝗲𝗮𝗻 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲 𝗯𝘆 𝗕𝗼𝗯 𝗠𝗮𝗿𝘁𝗶𝗻..

Links are in the comments.

\_\_\_\_\_\_\_  
If you like my posts please follow me Dr. Milan Milanović and hit the 🔔 on my profile to get a notification for all my new posts.

Grow with me 🚀\!

\#softwareengineering \#softwarearchitecture \#personaldevelopment \#books \#techworldwithmilan  
…see more

\=== POST 371 \===  
ziya mahammad  
View ziya mahammad’s profile  
   
• 2nd  
Engineering at Booking

3yr •   
3yr Visible to everyone

I often get DMs like how to become a backend developer.

As a backend developer, you will be responsible for building and maintaining the server side of web applications. 

Your work will involve designing and implementing the underlying architecture and APIs that power the application, as well as integrating with databases and other external services. 

Here are a few skills and technologies that you may want to consider learning as you progress in your career as a backend developer:

𝐏𝐫𝐨𝐠𝐫𝐚𝐦𝐦𝐢𝐧𝐠 𝐥𝐚𝐧𝐠𝐮𝐚𝐠𝐞𝐬: Start by learning a general-purpose programming language such as Python, Java, or C\#. These languages will give you a solid foundation in programming concepts and will allow you to build a wide range of applications.

𝐖𝐞𝐛 𝐝𝐞𝐯𝐞𝐥𝐨𝐩𝐦𝐞𝐧𝐭 𝐟𝐫𝐚𝐦𝐞𝐰𝐨𝐫𝐤𝐬: To build web applications, you will need to learn a web development framework such as Django, Spring, or ASP.NET. These frameworks provide a structure for building and deploying web applications, and they often include libraries and tools to help you with common tasks such as routing, authentication, and database access.

𝐃𝐚𝐭𝐚𝐛𝐚𝐬𝐞𝐬: As a backend developer, you will need to be proficient in working with databases. This will involve learning SQL and NoSQL and understanding how to design and query databases, as well as how to connect to them from your application. 

𝐀𝐏𝐈𝐬 𝐚𝐧𝐝 𝐦𝐢𝐜𝐫𝐨𝐬𝐞𝐫𝐯𝐢𝐜𝐞𝐬: You will also need to learn how to build APIs (Application Programming Interfaces) that allow other systems to interact with your application. This will involve understanding REST (Representational State Transfer)/gRPC and learning how to design and implement APIs that are scalable, secure, and easy to use.

𝐂𝐥𝐨𝐮𝐝 𝐜𝐨𝐦𝐩𝐮𝐭𝐢𝐧𝐠: Many backend developers work with cloud-based platforms such as Amazon Web Services (AWS), Microsoft Azure, or Google Cloud Platform (GCP). Learning how to build and deploy applications on these platforms will give you valuable skills and make you more attractive to potential employers.

𝐋𝐞𝐚𝐫𝐧 𝐚𝐛𝐨𝐮𝐭 𝐩𝐞𝐫𝐟𝐨𝐫𝐦𝐚𝐧𝐜𝐞 𝐚𝐧𝐝 𝐬𝐜𝐚𝐥𝐚𝐛𝐢𝐥𝐢𝐭𝐲: As your application grows in popularity, you will need to ensure that it can handle a large number of users and requests without slowing down. You should learn about techniques for optimizing the performance and scalability of your application.

𝐎𝐭𝐡𝐞𝐫 𝐬𝐤𝐢𝐥𝐥𝐬: There are many other skills and technologies that can be useful for backend developers, depending on the specific needs of the applications they are building. Some examples include:  
\- Containerization and orchestration (e.g., Docker, Kubernetes)  
\- Serverless computing  
\- Security and authentication (e.g., OAuth, JWT)  
\- Data processing and analytics (e.g., Hadoop, Spark)  
\- Integration with external services (e.g., payment gateways, messaging systems)

Let me know in the comment section if there is anything to add ✌🏻

ziya mahammad📍  
…see more

\=== POST 372 \===  
Rammohan Sundaram  
View Rammohan Sundaram’s profile  
   
• 2nd  
Founder & CEO \- KokoroBharat| 3X Entrepreneur| Doctorate Holder| Proud Alumni \- INSEAD, UCLA Anderson & SP. Jain| 3 Patents \- Blockchain in Adtech| ENTJ Personality

3yr •   
3yr Visible to everyone

Some understanding for those who would like to see visual representation of how some of these ConsumerTech companies make money.

PS: Infosys is about shareholding\!

\#ConsumerTech \#BusinessRevenue \#TechCompanies \#StartUp \#WhatsApp \#InvestyWise

Here is the link \-\> https://lnkd.in/dwjSVvQS  
…see more

\=== POST 373 \===  
Status is reachable  
Sunny Mishra  
View Sunny Mishra’s profile  
   
• 1st  
Engineering manager

3yr •   
3yr Visible to everyone

Career update: I accepted the offer of a Service company and will continue to work on the same Product and the same team I was working with previously, but now as a vendor.

Recently moved to lead a small team for Data Engineering and Application development. Since this requires a lot of upskilling, I have noted a set of technologies for my next 6 months' learning path.

Starting tomorrow morning at 5.30 am I will be hosting 1.5-hour-long Youtube live study sessions regularly where I will be studying a new technology Live. You can watch me, or utilize the time to learn something yourself.

The topic of tomorrow morning's study session is Apache Airflow.  
…see more

\=== POST 374 \===  
Thiago Ghisi  
View Thiago Ghisi’s profile  
   
• 2nd  
Sabbatical | (Former) Director of Engineering @ Nubank, Apple, Amex | Sharing: 🧗Career Growth Strategies,💡Eng. Leadership Insights & 📚My Curated Reads.

3yr •   
3yr Visible to everyone

I've read 500+ books and accumulated 55.000+ notes & highlights over the last ten years. 99% of those books were non-fiction & mostly around Software Engineering.

Below are the 22 Technical Books that Impacted my Career In Tech The Most with their Highest-density Chapters & Pages:

1️⃣ The Software Craftsman: Professionalism, Pragmatism, Pride by Sandro Mancuso.

2️⃣ Working Effectively with Legacy Code by Michael Feathers.

3️⃣ Working Effectively with Unit Tests by Jay Fields.

4️⃣ The Effective Engineer: How to Leverage Your Efforts In Software Engineering to Make a Disproportionate and Meaningful Impact by Edmond Lau. 

5️⃣ Impact Mapping: Making a Big Impact with Software Products and Projects by Gojko Adzic. 

6️⃣ How Google Tests Software by James Whittaker, Jason Arbon & Jeff Carollo.

7️⃣ Your Code as a Crime Scene: Use Forensic Techniques to Arrest Defects, Bottlenecks, and Bad Design in Your Programs by Adam Tornhill. 

8️⃣ Big Data: Principles and best practices of scalable realtime data systems by Nathan Marz. 

9️⃣ The DevOps Handbook: How to Create World-Class Agility, Reliability, & Security in Technology Organizations by @RealGeneKim, @jezhumble, @patrickdebois & @botchagalupe.

🔟 Accelerate: Building and Scaling High Performing Technology Organizations by @nicolefv, @jezhumble & @RealGeneKim.

1️⃣1️⃣ Team Topologies: Organizing Business and Technology Teams for Fast Flow by Matthew Skelton & Manuel.

1️⃣2️⃣ Growing Object-Oriented Software, Guided by Tests by @sf105 & @natpryce.

1️⃣3️⃣ Implementation Patterns by Kent Beck .

1️⃣4️⃣ Programming Interviews Exposed: Secrets to Landing Your Next Job by @monganmd, @giguere & Noah Suojanen.

1️⃣5️⃣ Peopleware: Productive Projects and Teams by Tom DeMarco & Tim Lister.

1️⃣6️⃣ When Will It Be Done? Lean-Agile Forecasting To Answer Your Customers' Most Important Question by Daniel Vacanti. 

1️⃣7️⃣ Lessons Learned in Software Testing: A Context-Driven Approach by @drcemkaner, @jamesmarcusbach & @bpettichord.

1️⃣8️⃣ Staff Engineer: Leadership Beyond the Management Track by Will Larson.

1️⃣9️⃣ Refactoring: Improving the Design of Existing Code by Martin Fowler.

2️⃣0️⃣ Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation by @jezhumble & @davefarley77.

2️⃣1️⃣ Effective Java by Joshua Bloch.

2️⃣2️⃣ The RSpec Book: Behaviour Driven Development with RSpec, Cucumber, and Friends by @dchelimsky, @dastels, @aslak\_hellesoy, @srbaker, @tastapod & @brynary.

Additional books I still want to write more on:

2️⃣3️⃣ Extreme Programming by Kent Beck. 

2️⃣4️⃣ The Staff Engineer’s Path by Tanya Reilly. 

2️⃣5️⃣ The Clean Coder by Robert Martin. 

2️⃣6️⃣ Software Architecture for Developers by Simon Brown.

\#softwareengineering \#tech \#career  
…see more

The 22 Technical Books That Impacted My Career in Tech The Most | Thiago Ghisi

typefully.com

\=== POST 375 \===  
Mohit Sehrawat  
View Mohit Sehrawat’s profile  
   
• 2nd  
DevOps Engineer | Azure, Docker, Kubernetes, Linux, Python | Full-Stack Background (React.js, MERN) | 85K+ LinkedIn Community

3yr •   
3yr Visible to everyone

Are you looking to work Remotely?

Here is a list of companies around the Globe that are remote friendly.

If you find it useful, give it a like and save it.

Also share it with your friends and colleagues out there.

Follow Mohit Sehrawat for more. 

𝐍𝐎𝐓𝐄: 𝐓𝐨 𝐠𝐞𝐭 𝐭𝐡𝐞 𝐥𝐢𝐬𝐭 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐢𝐧𝐛𝐨𝐱, 𝐦𝐞𝐧𝐭𝐢𝐨𝐧 𝐲𝐨𝐮𝐫 𝐦𝐚𝐢𝐥 𝐢𝐝 𝐢𝐧 𝐭𝐡𝐞 𝐜𝐨𝐦𝐦𝐞𝐧𝐭 𝐬𝐞𝐜𝐭𝐢𝐨𝐧

𝐇𝐚𝐬𝐡𝐭𝐚𝐠𝐬:  
\#work \#remote \#corporate \#companies \#hiring \#coding \#datastructures \#algorithm \#programming \#webdevelopment \#softwareengineer \#remotejob \#hiringalert \#share  
…see more

𝐑𝐞𝐦𝐨𝐭𝐞 𝐅𝐫𝐢𝐞𝐧𝐝𝐥𝐲 𝐂𝐨𝐦𝐩𝐚𝐧𝐢𝐞𝐬💯

\=== POST 376 \===  
Ashish Dey  
View Ashish Dey’s profile  
   
• 2nd  
Senior Software Engineering at Amazon | Microsoft, Expert in Distributed Systems

3yr •   
3yr Visible to everyone

Prepare system design not by watching system design videos but by watching videos of important fundamentals.

Things will automatically become easy for you.

List of must know fundamentals for system design interviews.

✅ Authentication and Authorization. 

✅ Different protocols: HTTPS, Web Socket, HTTP Long polling, Gossip protocol.

✅ Gateway, Load balancers, Reverse proxy. 

✅ Stateless servers and stateful servers

✅ Microservices and Monoliths

✅ Queues like Kafka, SQS, SNS, Azure event hub or any other queues.

✅ Cache and different cache implementations. Good to know about Redis and Memcached. 

✅ Different databases (SQL, NoSQL, File storage, Blob storage) 

✅ Compute techniques, distributed compute and stream processing. 

✅ CDN

There are certainly a lot more components which are important tools and must be covered. 

Below is the component diagram of some important fundamentals to cover to master any system design interviews.

Note: Below is not a design of any system but a component diagram to show how different components can be connected to make them work together.

Do comment if you think this list must contain some more components. 

\#madgos \#systemdesign \#interviewprep   
…see more

\=== POST 377 \===  
Status is reachable  
Sumit Bhanushali  
View Sumit Bhanushali’s profile  
   
• 1st  
Lead Engineer (SDE-3) @SprintMoney | Ex-Frappe | Ex-Servify

3yr •   
3yr Visible to everyone

I was always fascinated by the workings of Computers, Operating Systems and how Programming Languages are made in general but I never got the time or right motivation to invest my time on it as it mostly doesn't directly relate to professional work. 

But that itch of curiosity still remained and I somehow discovered course named nand2tetris where they have addressed this curiosity by teaching to build our own computer starting from logic gates then by implementing our own CPU, ALU, Programming Language and then building games like tetris using that language.

Interesting thing is that it is self contained course i.e no prerequisites are required and course duration is only of 14 weeks. I have started this course hoping I get what I have signed up for. 

Has anyone completed this course? is it worth it? 

\#nand2tetris \#programming \#operatingsystems \#softwaredevelopment \#computerscience   
…see more

\=== POST 378 \===  
Deepak Kumar  
View Deepak Kumar’s profile  
   
• 2nd  
AI Engineer | Building Production AI Systems | RAG • Agents • MCP | Github 22K⭐ OSS

3yr •   
3yr Visible to everyone

Developer productivity is so underrated. You can work 8 hours with all the distraction and achieve nothing significant at the end of day or instead work 4 hours focused.

Here are my 10 tips of staying focused and maximising your productivity which I generally practice :

👉 Set clear goals and priorities: Identify the most important tasks and focus on them first. This will help you stay focused and avoid wasting time on less important tasks.

👉 Use a task management tool: Using a tool like Notion, trello can help you keep track of your tasks and projects, and stay organised.

👉 Use keyboard shortcuts: Learning keyboard shortcuts can save you a lot of time, especially if you use them frequently.

👉 Automate repetitive tasks and invest in your environment setup \- Use tools like Jenkins or travis ci or write test cases to automate repetitive tasks and save time. Invest in tools/extensions/resources that streamline your workflow, such as code editors and debugging tools.

👉 Take breaks: It's important to take breaks and avoid burnout. 

👉 Avoid distractions: Turn off notifications on your phone and computer, and find a quiet place to work if possible. I use extension like Undistracted to block social sites. 

👉 Work in blocks of time: Setting aside specific blocks of time for work can help you stay focused and avoid multitasking and context switching ( don't be elon musk 😂 )

👉 Use the Pomodoro Technique: This technique involves working for 25 minutes and then taking a 5 minute break. After 4 Pomodoro cycles, I prefer to take a longer break to avoid burnout and eye strain. 

👉 Seek help when needed: Don't be afraid to ask for help when you get stuck on a problem. It's often faster to ask someone for help than to spend hours trying to figure it out on your own.

👉 Use dark mode : It helps a lot in reducing eye strain. 

and, last but not least get enough sleep 😴

How do you improve your productive as a developer ? Share them in the comments below\!

\#developer \#productivity   
…see more

\=== POST 379 \===  
ByteByteGo  
View company: ByteByteGo  
613K followers

3yr •   
3yr Visible to everyone

Popular interview question \- what are the 𝐝𝐢𝐟𝐟𝐞𝐫𝐞𝐧𝐜𝐞𝐬 between Redis and Memcached?

The diagram below illustrates the key differences.

Subscribe to our weekly newsletter to learn something new every week:   
https://bit.ly/3FEGliw  
   
\#systemdesign \#coding \#interviewtips  
.  
…see more

\=== POST 380 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗛𝗼𝘄 𝗗𝗡𝗦 𝗪𝗼𝗿𝗸𝘀?

What happens when you type https://website.com into your browser and press Enter? If you're a web developer or DevOps/platform engineer, this is something you should know.

The first thing that needs to be done is to translate this text-based domain into a machine-adapted numerical IP address. This is the role of a DNS server and it acts as a phonebook of the Internet. 

Here is what happens under the hood. Four servers work together to deliver an IP address to the client: recursive resolvers, root nameservers, TLD nameservers, and authoritative nameservers. The steps are following:

𝟭. 𝗗𝗡𝗦 𝗥𝗲𝘀𝗼𝗹𝘃𝗲𝗿: The users enter https://website.com into the browser and the first thing that happens is that this request hit the DNS Resolver. This server interacts with other DNS servers to find the correct IP address. 

𝟮. 𝗥𝗼𝗼𝘁 𝗻𝗮𝗺𝗲𝘀𝗲𝗿𝘃𝗲𝗿: Now, the DNS Resolver contacts Root Servers (there are 13 of them), which are controlled by various organizations, and delegated by ICANN. They handle requests for top-level domains (TLD). If a Root server cannot find results in its records or zone files, it will find a record for the .com TLD and give requesting entity the address of the name server for .com addresses.

𝟯. 𝗧𝗟𝗗 𝗦𝗲𝗿𝘃𝗲𝗿: Next, the DNS Resolver queriest TLD Server, which response with an IP address of the domain's authoritative nameserver. 

𝟰. 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘁𝗮𝘁𝗶𝘃𝗲 𝗻𝗮𝗺𝗲𝘀𝗲𝗿𝘃𝗲𝗿: After the query to a domain's authoritative nameserver, he will return the IP address of the origin server. In the final step, DNS Resolver passes the origin Server IP address back to the client, which the client can use to access the webpage requested in the first place.

Also, what could happen if DNS is returned from the 𝗰𝗮𝗰𝗵𝗲, to improve load times? DNS records can be cached in different locations. By default modern web browsers cache DNS records for a set amount of time. In the next step, the operating system can cache DNS records too, then router and ISP at the end. If the IP address is not found in the cache, the search with DNS resolver begins.

\_\_\_\_\_\_\_  
If you like my posts please follow me Dr. Milan Milanović and hit the 🔔 on my profile to get a notification for all my new posts.

Grow with me 🚀\!

\#softwareengineering \#programming \#developers \#dns \#techworldwithmilan  
…see more

\=== POST 381 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗕𝗲𝘀𝘁 𝗣𝗿𝗮𝗰𝘁𝗶𝗰𝗲𝘀 𝗶𝗻 𝗔𝗣𝗜 𝗗𝗲𝘀𝗶𝗴𝗻

In our daily work as software engineers, the majority of us utilize or create REST APIs. The standard method of communication between the systems is through APIs. Therefore, it's crucial to properly build REST APIs to avoid issues in the future. A well-defined API should be 𝗲𝗮𝘀𝘆 𝘁𝗼 𝘄𝗼𝗿𝗸 𝘄𝗶𝘁𝗵, 𝗰𝗼𝗻𝗰𝗶𝘀𝗲, 𝗮𝗻𝗱 𝗵𝗮𝗿𝗱 𝘁𝗼 𝗺𝗶𝘀𝘂𝘀𝗲.

Here are some general recommendations:

𝟭. 𝗨𝘀𝗲 𝗻𝗼𝘂𝗻𝘀 𝗶𝗻𝘀𝘁𝗲𝗮𝗱 𝗼𝗳 𝘃𝗲𝗿𝗯𝘀

Verbs should not be used in endpoint paths. Instead, the pathname should contain the nouns that identify the object that the endpoint that we are accessing or altering belongs to.

E.g., instead of using /𝚐𝚎𝚝𝙰𝚕𝚕𝙲𝚕𝚒𝚎𝚗𝚝𝚜 to fetch all clients, use /𝚌𝚕𝚒𝚎𝚗𝚝𝚜.

𝟮. 𝗨𝘀𝗲 𝗽𝗹𝘂𝗿𝗮𝗹 𝗿𝗲𝘀𝗼𝘂𝗿𝗰𝗲 𝗻𝗼𝘂𝗻𝘀

Try to use the plural form for resource nouns, because this fits all types of endpoints.

E.g., instead of using /𝚎𝚖𝚙𝚕𝚘𝚢𝚎𝚎/:𝚒𝚍/, use /𝚎𝚖𝚙𝚕𝚘𝚢𝚎𝚎𝚜/:𝚒𝚍/

𝟯. 𝗕𝗲 𝗰𝗼𝗻𝘀𝗶𝘀𝘁𝗲𝗻𝘁

When we say to be consistent, this means to be predictable. When we have one endpoint defined, others should behave in the same way. So, use the same case for resources, the same auth methods for all endpoints, use the same headers, use the same status codes, etc.

𝟰. 𝗞𝗲𝗲𝗽 𝗶𝘁 𝘀𝗶𝗺𝗽𝗹𝗲

We should make naming all endpoints to be resource-oriented, as they are. If we want to define an API for users, we would define it as:

/𝚞𝚜𝚎𝚛𝚜  
/𝚞𝚜𝚎𝚛𝚜/𝟷𝟸𝟺

So, the first API gets all users and the second one gets a specific user.

𝟱. 𝗨𝘀𝗲 𝗽𝗿𝗼𝗽𝗲𝗿 𝘀𝘁𝗮𝘁𝘂𝘀 𝗰𝗼𝗱𝗲𝘀

This one is super important. There are many HTTP status codes, but we usually use just some of them. Don't use too many, but use the same status codes for the same outcomes across the API, e.g., 

\- 200 for general sucess  
\- 201 for succesfull creation  
\- 400 for bad requests  
\- 401 for unauthorized requests  
\- 403 for missing permissions  
\- 404 for missing resources  
\- 5xx for internal errors

𝟲. 𝗗𝗼𝗻'𝘁 𝗿𝗲𝘁𝘂𝗿𝗻 𝗽𝗹𝗮𝗶𝗻 𝘁𝗲𝘅𝘁

REST APIs should accept JSON for request payload and also respond with JSON because it is a standard for transferring data. Yet, it is not enough just to return a body with JSON-formatted string, we need to specify a Content-Type header too to be application/json. The only exception is if we’re trying to send and receive files between the client and server.

And don't forget to 𝗱𝗼𝗰𝘂𝗺𝗲𝗻𝘁 𝗔𝗣𝗜, because API will be only good as its documentation. The docs should show examples of complete request/response cycles. Here we can use the OpenAPI definition as a source of truth.

If you want to start developing APIs, check Swagger and OpenAPI specifications, Postman, or Stoplight.

Check the other recommendations in the comments.

\#softwareengineering \#programming \#api \#apidesign \#techworldwithmilan  
…see more

\=== POST 382 \===  
Status is online  
Ron Fybish  
View Ron Fybish’s profile  
   
• 2nd  
Co-Founder @ Foundera.co | Turning Founders into Thought Leaders on LinkedIn

3yr •   
3yr Visible to everyone

𝗛𝗼𝘄 𝗦𝗦𝗟 𝘄𝗼𝗿𝗸𝘀? 🔐🔥

Bob has a website where people can order pizza, but what if someone steals Bob customer's data?

🆘 𝗧𝗵𝗮𝘁 𝗶𝘀 𝘄𝗵𝘆 𝗶𝘁 𝗶𝘀 𝗰𝗿𝘂𝗰𝗶𝗮𝗹 𝘁𝗼 𝗵𝗮𝘃𝗲 𝗮𝗻 𝗦𝗦𝗟  
𝘉𝘶𝘵 𝘸𝘩𝘢𝘵 𝘦𝘹𝘢𝘤𝘵𝘭𝘺 𝘪𝘴 𝘪𝘵?  
𝘏𝘰𝘸 𝘥𝘰𝘦𝘴 𝘪𝘵 𝘩𝘦𝘭𝘱?

📄 𝗦𝗦𝗟 𝘀𝘁𝗮𝗻𝗱𝘀 𝗳𝗼𝗿 𝗦𝗲𝗰𝘂𝗿𝗲 𝗦𝗼𝗰𝗸𝗲𝘁𝘀 𝗟𝗮𝘆𝗲𝗿  
SSL is a secure protocol that helps to send information safely over the Internet it creates an encrypted connection between the device of the visitor and your website.

📄 𝗬𝗼𝘂 𝗺𝘂𝘀𝘁 𝗳𝗶𝗿𝘀𝘁 𝗵𝗮𝘃𝗲 𝗮𝗻 𝗦𝗦𝗟 𝗖𝗲𝗿𝘁𝗶𝗳𝗶𝗰𝗮𝘁𝗲  
An SSL certificate is a digital file that verifies the ownership or authenticity of a website.

📊 𝗛𝗼𝘄 𝗱𝗼𝗲𝘀 𝗦𝗦𝗟 𝘄𝗼𝗿𝗸?

\- To provide a high degree of privacy, SSL encrypts data transmitted across the web. 

 \- SSL initiates an authentication process called a handshake between two communicating devices to ensure that both devices are really who they claim to be.

\- SSL also digitally signs data to provide data integrity, verifying that the data is not tampered with before reaching its intended recipient  
…see more

How SSL Works?

\=== POST 383 \===  
Hussein Nasser  
View Hussein Nasser’s profile  
   
• 3rd+  
Software Engineer | Talks about backend, databases and operating systems

3yr •   
3yr Visible to everyone

MongoDB internal Architecture

I’m a big believer that database systems share similar core fundamentals at their storage layer and understanding them allows one to compare different DBMS objectively. For example, How documents are stored in MongoDB is no different from how MySQL or PostgreSQL store rows.

In this article I discuss the evolution of MongoDB internal architecture on how documents are stored and retrieved focusing on the index storage representation. 

 https://lnkd.in/gWDZigxZ

\#mongodb \#database \#softwareengineering  
…see more

\=== POST 384 \===  
Saad Aslam  
View Saad Aslam’s profile  
   
• 2nd  
Tech Lead @ Turing | Top 1% Software Engineering Mentor featured on Times Square | Founder Tech تہوار

3yr •   
3yr Visible to everyone

In this checklist, I have compiled frequently asked INTERVIEW QUESTIONS based on my experience. So, let’s get started\!

To get the most out of the checklist, I’d recommend:

1-Going through all the common interview questions  
2-Checking out the situational interview questions section and learn how to answer questions that are relevant to you  
3-Learning what’s the idea behind behavioral interview questions, so you’re prepared to answer whatever the HR manager shoots at you.

Follow me Saad Aslam for more content on Interview Preparation, System Design, Competitive Programming and Personal Branding.

Good Luck for the interviews\!

\#competitiveprogramming \#learning \#hiring \#interviewpreparation  
…see more

Technical Interview Preparation

\=== POST 385 \===  
Arpit Bhayani  
View Arpit Bhayani’s profile  
   
• 2nd  
Principal Engineer II at Razorpay • databases • ex-Staff Engineer at GCP Memorystore and GCP Dataproc • creator of DiceDB • built and sold Profile.fyi • ex-Amazon Fast Data and DoE Unacademy

3yr •   
3yr Visible to everyone

Here is a 4-step process I follow to learn new technologies, tools, and frameworks ⚡

1\. I implement "Hello world" of, literally, every new thing I am learning, be it Databases, Libraries, or Frameworks.

2\. With enough experience, you can build an inherent understanding that does not require implementation; and this is where you can form dots just by skimming.

Note: reaching this stage requires continuous learning studying, and practicing.

3\. I study mostly from Research papers and Reference books. But if it is hard to understand something, I refer to blogs and videos that guide me in quickly forming the dots.

There are the 3 phases of understanding

 \- Beginner: Blogs and Tutorial Videos  
 \- Intermediate: Blogs and Conference  
 \- Advanced: Papers, Conference, Books

Everything I read is listed on my website, you may find them helpful

Books: arpitbhayani.me/bookshelf  
Papers: arpitbhayani.me/papershelf

4\. To form a deeper understanding, I take handwritten notes. The notes are detailed assuming I will be using them to teach others.

Putting myself in someone else's shoes helps me question my understanding and ensure I grasp the concept well.

Everyone is different; the above approach worked for me, so take it with a pinch of salt. I would recommend trying different methods and converging on your own method.

\#Engineering \#SystemDesign \#AsliEngineering  
…see more

\=== POST 386 \===  
Piyush Sharma  
View Piyush Sharma’s profile  
   
• 2nd  
Software Engineer II @ Microsoft | 42k+ LinkedIn | Mentored 250+ Software Developers | Ex-Amazon

3yr •   
3yr Visible to everyone

Recently came across some really helpful GitHub Repositories:

1\. Build Your Own X : https://lnkd.in/dx5vYYH4

\- Created by CodeCrafters, this is a compilation of well written, step-by-step guide of recreating our favourite technologies. Eg: Making your own Search Engine, Operating System, Docker and even Git.

2\. The Art of Command Line : https://lnkd.in/dv8a4Wbs

\- A command line guide for both beginners and experienced people which is primarily written for Linux but contains sections for ‘macOS only’ and ‘Windows only’ both.

3\. Developer Roadmap : https://lnkd.in/df4xPtP7

\- Created by Kamran Ahmed, this is the best repository to get roadmaps, guides and other educational content for the developers. It provides roadmaps to be a frontend, backend, android developer etc. and a lot more.

4\. Free Programming Books : https://lnkd.in/dfKhWw-R

\- Maintained by EbookFoundation, this is one of the most famous repositories of GitHub. It provides free ebooks on almost every programming topic, that too in different languages. It is created to promote the creation, distribution, archiving and sustainability of free books.

Better Ideas Welcome\! :)  
For more such posts, follow Piyush Sharma 🤍

\#technology \#linkedin \#softwareengineering \#productivity \#networking \#personaldevelopment \#jobhelp \#programming \#interviewpreparation \#github \#developer   
…see more

\=== POST 387 \===  
Deepak Kumar  
View Deepak Kumar’s profile  
   
• 2nd  
AI Engineer | Building Production AI Systems | RAG • Agents • MCP | Github 22K⭐ OSS

3yr •   
3yr Visible to everyone

As a developer, I was constantly frustrated by the limitations of traditional REST APIs. I spent hours trying to work around their inflexibility and slow performance, but nothing seemed to work.

Then, I discovered GraphQL. It was like a breath of fresh air\! With its intuitive and flexible query language, I was able to build APIs that were fast, efficient, and easy to use.

On this weekend, I have added a new chapter in my ebook, "API for Product Managers" on GraphQL. I have explained the what and why's of GraphQL here \- bit.ly/3W0QNaY

This is an absolutely free chapter\!   
…see more

\=== POST 388 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗪𝗵𝗮𝘁 𝗶𝘀 𝘁𝗵𝗲 𝗯𝗲𝘀𝘁 𝗯𝗼𝗼𝗸 𝘆𝗼𝘂 𝗲𝘃𝗲𝗿 𝗿𝗲𝗮𝗱 𝘁𝗵𝗮𝘁 𝗰𝗵𝗮𝗻𝗴𝗲𝗱 𝘆𝗼𝘂𝗿 𝗹𝗶𝗳𝗲 𝗼𝗿 𝗰𝗮𝗿𝗲𝗲𝗿 ?

Write in the comments...

\#technology \#softwareengineering \#career \#techworldwithmilan  
…see more

\=== POST 389 \===  
Addy Osmani  
View Addy Osmani’s profile  
   
• 2nd  
Director, Google Cloud AI. Best-selling Author. Speaker. AI, DX, UX. I want to see you win.

3yr •   
3yr Visible to everyone

Write about what you learn. It pushes you to understand topics better. Sometimes the gaps in our knowledge only become clear when explaining things to others.

Related to this is Bloom's Taxonomy shown in the illustration. This a well-known framework for categorizing and organizing learning objectives. Bloom's Taxonomy organizes learning objectives into six levels, ranging from the most basic level of remembering and understanding, to the most complex level of creating and evaluating.

Creating and writing falls into the highest level of Bloom's Taxonomy, known as the "creating" level. At this level, learners are expected to generate new ideas, write-ups and be able to evaluate the work of others. This level emphasizes originality and innovation, and requires learners to think critically and independently.

Bloom's Taxonomy (revised) consists of:

1\. Remembering: recall or recognize previously learned information.  
2\. Understanding: comprehend the meaning of the material, and to be able to explain it in their own words.  
3\. Applying: use the material in a new context, such as solving a problem or making a decision.  
4\. Analyzing: breaking the material down into its component parts, and identifying the relationships among them.  
5\. Evaluating: make judgments about the value or quality of the material, based on a set of criteria.  
6\. Creating: generate write-ups, new ideas, or methods, and evaluate the work of others. This level emphasizes originality and innovation.

I tend to find that writing about what you learn is a helpful forcing function for understanding how close to \#6 you are. Sometimes you may only be able to recall information, but not yet fully understand or apply it. Other times you may be able to apply it, but not yet be able to critically analyze and evaluate it (e.g. critique). Bloom’s taxonomy can be helpful for evaluating how well you understand topics.

\#softwareengineering \#learning \#productivity 

…see more

\=== POST 390 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗪𝗵𝗮𝘁 𝗶𝘀 𝗛𝗶𝗴𝗵-𝗾𝘂𝗮𝗹𝗶𝘁𝘆 𝗪𝗼𝗿𝗸 𝗶𝗻 𝗦𝗼𝗳𝘁𝘄𝗮𝗿𝗲 𝗘𝗻𝗴𝗶𝗻𝗲𝗲𝗿𝗶𝗻𝗴?

Yesterday we had a talk where I talked about what is High-quality work in software engineering and what is not. There is a lot of thought on this. Is it enough to work in Scrum? Or we also need to do clean code and TDD? We need to use functional programming? Well, there is no silver bullet.

Here I will reflect on a few important topics:

𝟭. 𝗚𝗿𝗲𝗮𝘁 𝗧𝗲𝗮𝗺

Every great project starts with a great team. We need people who are skilled in their job, who has a can-do attitude, and who know how to receive feedback.

𝟮. 𝗖𝘂𝘀𝘁𝗼𝗺𝗲𝗿 𝗙𝗼𝗰𝘂𝘀

We must focus on the customer. Customer is not usually interested in our tech stack, but in building the right product. We as engineerings want to build the product right. So we need a plan and work on it.

𝟯. 𝗜𝘁𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗺𝗲𝗻𝘁

We need some kind of iterative development. It doesn't need to be Scrum (it has its drawbacks), but we need some kind of a process that will result in working software.

𝟰. 𝗖𝗼𝗻𝘁𝗶𝗻𝗼𝘂𝘀 𝗗𝗲𝗽𝗹𝗼𝘆𝗺𝗲𝗻𝘁

We want to deploy our software at the end of every iteration to production, or at least to the testing environment, but at the same time, we want to continue working on our features. We can do this by separating releases from deployment. This can be done e.g., with feature flags.

𝟱. 𝗦𝗶𝗺𝗽𝗹𝗲 𝗗𝗲𝘀𝗶𝗴𝗻

When we start with a project we want to design the system. Here a suggestion is to start with a simple design and iterate. Create it through system design reviews and get feedback from colleagues. It is much better to go with a simple design than to use some shiny architectural patterns.

Here a modular monolith behind an API Gateway, which can be later split into separate services.

𝟲. 𝗙𝗶𝗴𝗵𝘁𝗶𝗻𝗴 𝗧𝗲𝗰𝗵 𝗗𝗲𝗯𝘁

As our work on the project continues tech debt is rising. There are different kinds of tech debt, such as bad code, no tests, unused features, manual processes, or lack of knowledge sharing. We can fight it by empowering the team to fix problems and to do this without asking for permission. This will make us a bit slower but we will gain more in the future.

𝟳. 𝗕𝗮𝗱 𝗰𝗼𝗱𝗲

The question is why we write bad code. There are different reasons for that (time pressure, already bad codebase, etc.), but we can do something about it. Try the Boy Scout rule, coined by Uncle Bob Martin. Every time you open an editor to do something, do a small refactoring, rename a variable, extract a method or add a missing test.

We also need to have a proper engineering culture and practices. For more about this, check the presentation.

And in the end, don't just do. To become an expert we need time and we need to fail and learn and to again.

\#softwareengineering \#programming \#developers \#technology \#techworldwithmilan  
…see more

High Quality Work in Software Engineering

\=== POST 391 \===  
Rocky Bhatia  
View Rocky Bhatia’s profile  
   
• 2nd  
400K+ Engineers | Architect @ Adobe | GenAI & Systems at Scale

3yr •   
3yr Visible to everyone

One Diagram For Software Architectural Design Pattern 

In software engineering, a software design pattern is a general, reusable solution of how to solve a common problem when designing an application or system. Unlike a library or framework, which can be inserted and used right away, a design pattern is more of a template to approach the problem at hand.

14 Important and widely used design Patterns to follow :

𝟭. 𝗦𝘁𝗮𝘁𝗶𝗰 𝗖𝗼𝗻𝘁𝗲𝗻𝘁 𝗛𝗼𝘀𝘁𝗶𝗻𝗴: used to optimize webpage loading time. It stores static content (information that doesn't change often, like an author's bio or an MP3 file) separately from dynamic content (like stock prices).

𝟮. 𝗣𝗲𝗲𝗿-𝘁𝗼-𝗣𝗲𝗲𝗿: Involves multiple components called Peers, where a pear may function both as a client, requesting services from other peers, and as a server, providing services to other peers.

𝟯. 𝗣𝘂𝗯𝗹𝗶𝘀𝗵𝗲𝗿-𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲𝗿: Used to send (publishes) relevant messages to places that have subscribed to a topic.

𝟰. 𝗦𝗵𝗮𝗿𝗱𝗶𝗻𝗴 𝗣𝗮𝘁𝘁𝗲𝗿𝗻 – Used to partition data in a database to speed commands or queries.

𝟱. 𝗖𝗶𝗿𝗰𝘂𝗶𝘁 𝗕𝗿𝗲𝗮𝗸𝗲𝗿: Helps make systems more fault tolerant by minimizing the effects of a hazard by rerouting traffic to another service.

𝟲. 𝗟𝗮𝘆𝗲𝗿𝗲𝗱 𝗣𝗮𝘁𝘁𝗲𝗿𝗻: Generally used to develop applications that include groups of subtasks that execute in a specific order.

𝟳. 𝗖𝗹𝗶𝗲𝗻𝘁-𝗦𝗲𝗿𝘃𝗲𝗿: A peer-to-peer architecture that is comprised of a client, which requests a service, and a server, which provides the service.

𝟴. 𝗠𝗮𝘀𝘁𝗲𝗿-𝗦𝗹𝗮𝘃𝗲: Consists of two components; the master distributes the work among identical slaves and computes a final result from the results which the slaves return.

𝟵. 𝗣𝗶𝗽𝗲-𝗙𝗶𝗹𝘁𝗲𝗿: Used to structure systems that produce and process a stream of data.

𝟭𝟬. 𝗘𝘃𝗲𝗻𝘁-𝗗𝗿𝗶𝘃𝗲𝗻: Uses events to trigger and communicate between decoupled services.

𝟭𝟭. 𝗠𝗼𝗱𝗲𝗹-𝗩𝗶𝗲𝘄-𝗖𝗼𝗻𝘁𝗿𝗼𝗹𝗹𝗲𝗿: Divides an application into three components. The model contains the application's data and main functionality; the view displays data and interacts with the user; and the controller handles user input and acts as the mediator between the model and the view.

𝟭𝟮. Throttling \- pattern controls how fast data flows into a target. It's often used to prevent failure during a distributed denial of service attack or to manage cloud infrastructure costs..

𝟭𝟯. 𝗠𝗶𝗰𝗿𝗼𝘀𝗲𝗿𝘃𝗶𝗰𝗲𝘀: Used to create multiple services that work interdependently to create a larger application.

𝟭𝟰. 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗤𝘂𝗲𝗿𝘆 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗶𝗯𝗶𝗹𝗶𝘁𝘆 𝗦𝗲𝗴𝗿𝗲𝗴𝗮𝘁𝗶𝗼𝗻: Used to separate read and write activities to provide greater stability, scalability, and performance.

Text Credits https://lnkd.in/dhYXhTVk

\#architecture \#designpatterns \#software \#softwareengineering \#softwarearchitecture \#interviewingtips \#systemdesign \#learningdesign \#learningeveryday   
…see more

\=== POST 392 \===  
Manish Gupta  
View Manish Gupta’s profile  
   
• 2nd  
Principal Applied Scientist at Microsoft, Adjunct Faculty at IIITH+IITJ, Visiting Faculty at ISB, Board Member of TIH@IIT Patna

3yr •   
3yr Visible to everyone

Hi folks,

In the spirit of lifelong learning and sharing learnings, I have started recording some of the latest pieces of breakthrough research.  
Current interest areas are deep learning for NLP and vision.

In case the following topics interest you, please feel free to visit https://lnkd.in/gZCUNTYs  
I plan to record at least 1 video per week; hence, please feel free to subscribe. Feedback/suggestions welcome.

\-- T0, T0+, T0++, BLOOMZ and mT0: Multi-task Prompted Finetuning  
\-- Amazon Research Days presentation on Designing a Query Auto-Completion System  
\-- DALL-E: Zero-Shot Text-to-Image Generation  
\-- DDPM: Denoising Diffusion Probabilistic Models  
\-- OpenAI InstructGPT: Training language models to follow instructions with human feedback  
\-- Chain of thought prompting to solve Big Bench Hard tasks  
\-- Deep Learning for Brain Encoding and Decoding  
\-- BIG bench Beyond the Imitation Game benchmark  
\-- Handling Defective Suggestions and Prefixes in Query Auto Completion Systems  
\-- Personalization for Query Auto Completion Systems  
\-- Natural Language Generation for Query Auto Completion Systems  
\-- Ranking in Query Auto Completion Systems  
\-- Designing a Query Auto Completion System

\#learning \#nlp \#deeplearning \#DataScience \#youtube   
…see more

\=== POST 393 \===  
Chirag Goel  
View Chirag Goel’s profile  
   
• 2nd  
Principal Engineering Manager at Microsoft | ex-Flipkart | Teacher | Mentor | YouTuber 🚀

3yr •   
3yr Visible to everyone

Are you worried about layoffs? Start doing this 👇  
.  
.  
.  
.  
.  
1\. Update Your Skills: One powerful way to defend yourself against layoffs is to be as proficient as possible in your current job, as well as to think ahead and stay current in your field. If you haven’t done so in a while, take some classes to update your skills.

2\. Enhance Your Network: Make sure that you’re connected to the people in your industry. Getting plugged into discussion lists, attending conferences and networking events regularly, and connecting to people on social media sites are all great ways to keep your finger on the pulse of your industry.

3\. Build Up Visibility: If you do decide to reach out for new roles, be sure to do it in a strategic way. Make sure to build your personal brand on social media and in professional circles. Focus on showcasing your skills, rather than just listing them on your resume.

4\. Have Open Dialogue with Your Colleagues: Discussing the issues with your colleagues could help the company avoid layoffs. Consider talking to your peers to discover ways they’re actively trying to increase the business.

5\. Seek Out Multiple Sources of Income: Having multiple sources of income is not only important for job security, but it also helps you reach financial security. It’s important to diversify your skills and even industries so that you’re not reliant on one source of income.

Do share in your network to help others 👨‍💻

To enhance your skill follow the link in the comment 👇

\#layoff \#security \#softwareengineers \#job

…see more

\=== POST 394 \===  
Arslan Ahmad  
View Arslan Ahmad’s profile  
   
• 2nd  
Author of Bestselling ‘Grokking’ Series on System Design, Software Architecture & Coding Patterns | Founder DesignGurus.io

3yr •   
3yr Visible to everyone

𝗦𝘆𝘀𝘁𝗲𝗺 𝗗𝗲𝘀𝗶𝗴𝗻 𝗕𝗮𝘀𝗶𝗰𝘀: 𝗪𝗵𝗮𝘁 𝗶𝘀 𝗮𝗻 𝗔𝗣𝗜 𝗚𝗮𝘁𝗲𝘄𝗮𝘆?

An API gateway is a server that acts as a single point of entry for a set of \#microservices. 

It receives client requests, forwards them to the appropriate microservice, and then returns the server's response to the client.

The API gateway is responsible for tasks such as routing, authentication, and rate limiting. This enables microservices to focus on their individual tasks and improves the overall performance and scalability of the system.

API gateways are used for a variety of purposes in microservice architectures, including the following:

𝗥𝗼𝘂𝘁𝗶𝗻𝗴: The API gateway receives requests from clients and routes them to the appropriate microservice. This enables clients to access the various microservices through a single entry point, simplifying the overall system design.

𝗔𝘂𝘁𝗵𝗲𝗻𝘁𝗶𝗰𝗮𝘁𝗶𝗼𝗻: The API gateway can be used to authenticate clients and enforce access control policies for the microservices. This helps to ensure that only authorized clients can access the microservices and helps to prevent unauthorized access.

𝗥𝗮𝘁𝗲 𝗹𝗶𝗺𝗶𝘁𝗶𝗻𝗴: You can rate limit client access to microservices with an API gateway. This can help prevent denial of service attacks and other types of malicious behavior.

𝗟𝗼𝗮𝗱 𝗯𝗮𝗹𝗮𝗻𝗰𝗶𝗻𝗴: The API gateway can distribute incoming requests among multiple instances of a microservice, enabling the system to handle a larger number of requests and improving its overall performance and scalability.

𝗖𝗮𝗰𝗵𝗶𝗻𝗴: The API gateway can cache responses from the microservices, reducing the number of requests that need to be forwarded to the microservices and improving the overall performance of the system.

𝗠𝗼𝗻𝗶𝘁𝗼𝗿𝗶𝗻𝗴: The API gateway can collect metrics and other data about requests and responses, providing valuable insights into the performance and behavior of the microservices. This can help to identify and diagnose problems, and improve the overall reliability and resilience of the system.

\#systemdesign \#microservices \#api \#apigateway   
…see more

\=== POST 395 \===  
Tobias Zwingmann  
View Tobias Zwingmann’s profile  
   
• 2nd  
Author: The Profitable AI Advantage. Created profits with AI from enterprise giants to 20-person teams.

3yr •   
3yr Visible to everyone

ChatGPT 3 is out and the internet is exploding\! 🤯 

I spent 3 hrs on Twitter finding the most popular use cases. 

Here’s my Top 10 list:

1 Use ChatGPT instead of Google search:  
https://lnkd.in/eBNbEpJH

2 Use ChatGPT to explain complex algorithms in any teaching style you want:  
https://lnkd.in/eVK3N9hP

3 Use ChatGPT to create prompts for DALL-E/StableDiffusion. This is so 🤯  
https://lnkd.in/e9f-Zmbj

4 Let ChatGPT help you build apps from scratch  
https://lnkd.in/e5zdsNpb

5 Let ChatGPT explain scientific concepts  
https://lnkd.in/efHU\_yHC

6 Stich cloud services together:  
https://lnkd.in/e3dGQYVM

7 Write recipes\! 😋   
https://lnkd.in/ecpAkFz8

8 Solve homework assignments:  
https://lnkd.in/eZ5tJdcs

9 Write humorous stories:  
https://lnkd.in/etRed\_zg

10 Skip StackOverflow and go directly to the answer  
https://lnkd.in/er9YtxWj

If you haven’t heard:

ChatGPT is a large language model (LLM) trained by OpenAI that's capable of generating human-like text in response to user input and remembering what the user said earlier in the conversation so it can make follow-up corrections.

ChatGPT is fine-tuned from a model in the GPT-3.5 series, which finished training in early 2022\.

Key capabilities:   
\- Remembers what user said earlier in the conversation  
\- Allows user to provide follow-up corrections  
\- Trained to decline inappropriate requests

Key Limitations:  
\- May occasionally generate incorrect information  
\- May occasionally produce harmful instructions or biased content  
\- Limited knowledge of world and events after 2021

You can learn more about ChatGPT here: https://lnkd.in/etV5uYdc

Which \#ChatGPT use case makes your eyes light up?

\#ai \#innovation   
…see more

\=== POST 396 \===  
Status is online  
Ron Fybish  
View Ron Fybish’s profile  
   
• 2nd  
Co-Founder @ Foundera.co | Turning Founders into Thought Leaders on LinkedIn

3yr •   
3yr Visible to everyone

Get started with Nginx 🔋🔥 

Bob had always been a savvy businessman. Bob started his own online store, and within just a few months, it was doing incredibly well. 🚀

🐸 Bob's website got 10,000 visitors in one day. The server couldn't handle all the traffic, and it crashed. 

🐸 The main problem that web servers commonly face were heavy loads. With more connections-the webserver slows down. 

🐸 𝗟𝘂𝗰𝗸𝗶𝗹𝘆 𝗳𝗼𝗿 𝗕𝗼𝗯, 𝗵𝗲 𝗵𝗮𝗱 𝗵𝗲𝗮𝗿𝗱 𝗮𝗯𝗼𝘂𝘁 𝗡𝗴𝗶𝗻𝘅, a web server with different features to handle this problem. 

🐸 𝗡𝗴𝗶𝗻𝘅 can efficiently distribute requests among multiple processors and memory caches. Which means it can handle significantly more connections than traditional web servers. 

🐸 Bob quickly installed \#nginx on her server and was back up and running in no time\! 

🐸 Bob's website continued to experience record traffic numbers, and Bob could keep up with demand thanks to Nginx's powerful performance capabilities.

…see more

Get started with Nginx

\=== POST 397 \===  
Nitesh Yadav  
View Nitesh Yadav’s profile  
   
• 2nd  
SWE @Meta l Ex-Amazon | doing some tech stuff

3yr •   
3yr Visible to everyone

Do you want to learn, how to code?  
looking for resources?  
Want to crack interviews or improve your CP skills?

No matter whether you are a beginner or not. The below list is the ultimate resource to learn data structures and algorithm that improves your problem-solving skills.

📌 Analysis of Algorithms: https://lnkd.in/d6XjwbBy

📌 Tree: https://lnkd.in/dgSGnTSD

📌 Stacks: https://lnkd.in/dErHXVgb

📌 Sorting: https://lnkd.in/d\_kx9ffG

📌 Recursion: https://lnkd.in/djASWqrW

📌 Randomized Algorithms: https://lnkd.in/dy78NzYT

📌 Priority queue: https://lnkd.in/drzwvMrE

📌 Matrix: https://lnkd.in/dfEy4Yq6

📌 Linked List: https://lnkd.in/dbd3j9pi

📌 Heap: https://lnkd.in/d8yMqiw9

📌 Hashing: https://lnkd.in/dz6D7F\_v

📌 Greedy Algo: https://lnkd.in/dqdixCGi

📌 Graphs: https://lnkd.in/dC\_Aqg28

📌 Geometry: https://lnkd.in/drNM98UN

📌 Game Theory: https://lnkd.in/dRGspjEV

📌 DP: https://lnkd.in/dwcXCeu5

📌 Design Pattern: https://lnkd.in/dnNbFWNS

📌 CP tips and tricks: https://lnkd.in/dvAt\_iYn

📌 Combinatorics: https://lnkd.in/d9K\_ZQgM

📌 BST: https://lnkd.in/deqYktzh

📌 BS and D\&C: https://lnkd.in/dR7aeSZG

📌 Bits: https://lnkd.in/dCc7jPNA

📌 Backtracking: https://lnkd.in/dvRDPNwZ

📌 Pattern Finding: https://lnkd.in/dzpE-JmK

📌 Some Tips: https://lnkd.in/dEgbX\_jh

Share, like, and comment. So, everyone gets benefits from it.

Please Subscribe to my channel:  
https://lnkd.in/eGnbAjgs

Thank you 😊

\#algorithms \#datastructures   
…see more

\=== POST 398 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗪𝗵𝗮𝘁 𝗵𝗮𝗽𝗽𝗲𝗻𝘀 𝘄𝗵𝗲𝗻 𝘆𝗼𝘂 𝘁𝘆𝗽𝗲 𝗮 𝗨𝗥𝗟 𝗶𝗻𝘁𝗼 𝘆𝗼𝘂𝗿 𝗯𝗿𝗼𝘄𝘀𝗲𝗿?

The process involves the browser, your computer’s operating system, your internet service provider, the server where you host the site, and the services running on that server.

𝟭. 𝗬𝗼𝘂 𝘁𝘆𝗽𝗲 𝗵𝘁𝘁𝗽𝘀://𝘀𝗼𝗺𝗲𝘄𝗲𝗯𝘀𝗶𝘁𝗲.𝗰𝗼𝗺/𝗽𝗮𝗴𝗲 𝗶𝗻 𝘆𝗼𝘂𝗿 𝗯𝗿𝗼𝘄𝘀𝗲𝗿 𝗮𝗻𝗱 𝗽𝗿𝗲𝘀𝘀 𝗘𝗻𝘁𝗲𝗿

Here, https:// is a scheme, which tells the browser to make a connection to the server using TLS. somewebsite.com is the domain name of the site and it points to a specific IP address of a server. And /page is a path to the resource you need.

𝟮. 𝗕𝗿𝗼𝘄𝘀𝗲𝗿 𝗹𝗼𝗼𝗸𝘀 𝘂𝗽 𝗜𝗣 𝗮𝗱𝗱𝗿𝗲𝘀𝘀 𝗳𝗼𝗿 𝘁𝗵𝗲 𝗱𝗼𝗺𝗮𝗶𝗻

After you’ve typed the URL into your browser and pressed enter, the browser needs to figure out which server on the Internet to connect to. It must look for the IP address of the server hosting the website using the domain you typed to accomplish that. DNS lookup is used to do this. Here, it determines whether we can locate it in the cache; if not, DNS must search domain name servers from the root to the third level.

𝟯. 𝗕𝗿𝗼𝘄𝘀𝗲𝗿 𝗶𝗻𝗶𝘁𝗶𝗮𝘁𝗲𝘀 𝗧𝗖𝗣 𝗰𝗼𝗻𝗻𝗲𝗰𝘁𝗶𝗼𝗻 𝘄𝗶𝘁𝗵 𝘁𝗵𝗲 𝘀𝗲𝗿𝘃𝗲𝗿

Transmission control protocol, more formally known as TCP, is used throughout the public Internet routing infrastructure to route packets from a client browser request through the router, the Internet service provider, through an internet exchange to switch ISPs or networks, and finally to find the server with the IP address to connect to. This is an inefficient oute to take to get there. Instead, a lot of websites employ a CDN to cache both static and dynamic material closer to the browser.

𝟰. 𝗕𝗿𝗼𝘄𝘀𝗲𝗿 𝘀𝗲𝗻𝗱𝘀 𝘁𝗵𝗲 𝗛𝗧𝗧𝗣 𝗿𝗲𝗾𝘂𝗲𝘀𝘁 𝘁𝗼 𝘁𝗵𝗲 𝘀𝗲𝗿𝘃𝗲𝗿

Now that the browser is connected to the server, it complies with the HTTP(s) protocol's requirements for communication. To request the contents of the page, the browser first sends an HTTP request to the server. The body, headers, and request line of an HTTP request are all present. The server can determine what the client wants to do using the information in the request line.

𝟱. 𝗦𝗲𝗿𝘃𝗲𝗿 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗲𝘀 𝗿𝗲𝗾𝘂𝗲𝘀𝘁 𝗮𝗻𝗱 𝘀𝗲𝗻𝗱𝘀 𝗯𝗮𝗰𝗸 𝗮 𝗿𝗲𝘀𝗽𝗼𝗻𝘀𝗲

The server accepts the request and determines how to handle it depending on the data in the request line, headers, and body. The server receives the material at this URL for the GET /page/ HTTP/1.1 requests, builds the response, and then delivers it back to the client with an HTTP status code.

𝟲. 𝗕𝗿𝗼𝘄𝘀𝗲𝗿 𝗿𝗲𝗻𝗱𝗲𝗿𝘀 𝘁𝗵𝗲 𝗰𝗼𝗻𝘁𝗲𝗻𝘁

The browser examines the response headers for instructions on how to render the resource after receiving the server's response. The Content-Type header informs the browser that an HTML resource was received in the response body. 

Image credits: @manekinekko.

\#softwareengineering \#programming \#techwoldwithmilan  
…see more

\=== POST 399 \===  
Addy Osmani  
View Addy Osmani’s profile  
   
• 2nd  
Director, Google Cloud AI. Best-selling Author. Speaker. AI, DX, UX. I want to see you win.

3yr •   
3yr Visible to everyone

The Feynman Technique is great model for learning anything better.  
   
It’s a method of learning and understanding complex subjects by breaking them down into their simplest components and explaining them in plain language, named after the physicist Richard Feynman. 

The technique involves four steps:  
1\. Choose a concept or idea that you want to learn about.  
2\. ELI5 (Explain It To Me Like I'm 5). Pretend that you are explaining the concept to someone who knows nothing about it. Write out your explanation in simple, plain language, using examples and analogies to make it easier to understand.  
3\. Review your explanation and look for any gaps or unclear points. Go back to the original source material (such as a textbook or lecture notes) and fill in any gaps in your understanding.  
4\. Simplify your explanations. Test your understanding by trying to explain the concept to someone else, or by asking a friend or colleague to listen to your explanation and provide feedback.

The Feynman Technique can can help you identify any gaps in your understanding and ensure that you have a deep and thorough understanding of the subject. I've found it valuable for retaining crucial information and knowledge and I hope you find it helpful too.

\#softwareengineering \#learning \#knowledge   
…see more

\=== POST 400 \===  
Ansh Mishra  
View Ansh Mishra’s profile  
   
• 2nd  
Developer @Futures First | Quant

3yr •   
3yr Visible to everyone

𝐈𝐟 𝐲𝐨𝐮 𝐚𝐫𝐞 𝐢𝐧𝐭𝐨 𝐂𝐨𝐦𝐩𝐞𝐭𝐢𝐭𝐢𝐯𝐞 𝐏𝐫𝐨𝐠𝐫𝐚𝐦𝐦𝐢𝐧𝐠 𝐨𝐫 𝐢𝐧𝐭𝐨 𝐚𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐃𝐒𝐀 𝐨𝐩𝐭𝐢𝐦𝐢𝐳𝐚𝐭𝐢𝐨𝐧𝐬 𝐭𝐡𝐞𝐧 𝐭𝐡𝐢𝐬 𝐩𝐨𝐬𝐭 𝐢𝐬 𝐟𝐨𝐫 𝐲𝐨𝐮.

Proficiency in Mathematics is one thing that can always give you an upper edge in big-league contests or even day-to-day optimizations.   
So here are a few Blogs prepared on CodeForces by coders like 𝐈𝐧𝐭𝐞𝐫𝐧𝐚𝐭𝐢𝐨𝐧𝐚𝐥 𝐆𝐫𝐚𝐧𝐝 𝐌𝐚𝐬𝐭𝐞𝐫, 𝐚𝐧𝐝 𝐈𝐧𝐭𝐞𝐫𝐧𝐚𝐭𝐢𝐨𝐧𝐚𝐥 𝐌𝐚𝐬𝐭𝐞𝐫 on optimizations via leveraging math.

𝟏) 𝐍𝐮𝐦𝐛𝐞𝐫 𝐓𝐡𝐞𝐨𝐫𝐲 𝐢𝐧 𝐂𝐨𝐦𝐩𝐞𝐭𝐢𝐭𝐢𝐯𝐞 𝐏𝐫𝐨𝐠𝐫𝐚𝐦𝐦𝐢𝐧𝐠 \[𝐓𝐮𝐭𝐨𝐫𝐢𝐚𝐥\]  
Link: https://lnkd.in/dp4ShgAM

𝟐)𝐅𝐚𝐬𝐭 𝐦𝐨𝐝𝐮𝐥𝐚𝐫 𝐦𝐮𝐥𝐭𝐢𝐩𝐥𝐢𝐜𝐚𝐭𝐢𝐨𝐧  
Link: https://lnkd.in/dRE8Z-KU

𝟑)𝐎(𝟏) 𝐫𝐮𝐧𝐭𝐢𝐦𝐞 𝐩𝐫𝐢𝐦𝐞 𝐜𝐡𝐞𝐜𝐤𝐢𝐧𝐠  
Link: https://lnkd.in/d86sF\_Pd

𝟒)𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐢𝐧𝐠 𝐅𝐮𝐧𝐜𝐭𝐢𝐨𝐧𝐬 𝐢𝐧 𝐂𝐨𝐦𝐩𝐞𝐭𝐢𝐭𝐢𝐯𝐞 𝐏𝐫𝐨𝐠𝐫𝐚𝐦𝐦𝐢𝐧𝐠 (𝐏𝐚𝐫𝐭 𝟏)  
Link: https://lnkd.in/d83j5U5H

5)𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐢𝐧𝐠 𝐅𝐮𝐧𝐜𝐭𝐢𝐨𝐧𝐬 𝐢𝐧 𝐂𝐨𝐦𝐩𝐞𝐭𝐢𝐭𝐢𝐯𝐞 𝐏𝐫𝐨𝐠𝐫𝐚𝐦𝐦𝐢𝐧𝐠 (𝐏𝐚𝐫𝐭 2\)  
Link: https://lnkd.in/dCnjr4uK

𝟔)𝐂𝐨𝐮𝐧𝐭𝐢𝐧𝐠 𝐃𝐢𝐯𝐢𝐬𝐨𝐫𝐬 𝐨𝐟 𝐚 𝐍𝐮𝐦𝐛𝐞𝐫 𝐢𝐧 𝐎(𝐍^𝟏/𝟑)  
Link: https://lnkd.in/d4uFnvc4

𝟕)𝐂𝐚𝐭𝐚𝐥𝐚𝐧 𝐍𝐮𝐦𝐛𝐞𝐫𝐬 𝐚𝐧𝐝 𝐂𝐚𝐭𝐚𝐥𝐚𝐧 𝐂𝐨𝐧𝐯𝐨𝐥𝐮𝐭𝐢𝐨𝐧  
Link: https://lnkd.in/d98GV6KK

𝟖)𝐂𝐚𝐥𝐜𝐮𝐥𝐚𝐭𝐞 𝐦𝐨𝐝𝐮𝐥𝐨 𝐢𝐧𝐯𝐞𝐫𝐬𝐞𝐬 𝐞𝐟𝐟𝐢𝐜𝐢𝐞𝐧𝐭𝐥𝐲\!  
Link: https://lnkd.in/drz6yqx5

𝟗)𝐎𝐩𝐞𝐫𝐚𝐭𝐢𝐨𝐧𝐬 𝐨𝐧 𝐅𝐨𝐫𝐦𝐚𝐥 𝐏𝐨𝐰𝐞𝐫 𝐒𝐞𝐫𝐢𝐞𝐬  
Link: https://lnkd.in/duH8\_ni4

𝟏𝟎)𝐀𝐧 𝐞𝐟𝐟𝐢𝐜𝐢𝐞𝐧𝐭 𝐰𝐚𝐲 𝐭𝐨 𝐬𝐨𝐥𝐯𝐞 𝐬𝐨𝐦𝐞 𝐜𝐨𝐮𝐧𝐭𝐢𝐧𝐠 𝐩𝐫𝐨𝐛𝐥𝐞𝐦𝐬 𝐰𝐢𝐭𝐡𝐨𝐮𝐭 𝐦𝐚𝐭𝐫𝐢𝐱 𝐦𝐮𝐥𝐭𝐢𝐩𝐥𝐢𝐜𝐚𝐭𝐢𝐨𝐧  
Link: https://lnkd.in/dfF3Tgdp

Follow Ansh Mishra for more such Technical Content.

\#competitiveprogramming \#codeforces \#icpc \#dsa \#interviewpreparation \#programming \#softwareengineer   
…see more

\=== POST 401 \===  
Hussein Nasser  
View Hussein Nasser’s profile  
   
• 3rd+  
Software Engineer | Talks about backend, databases and operating systems

3yr •   
3yr Visible to everyone

I thought I understood how VPNs work until I saw this diagram. 

I’m not even close  
…see more

\=== POST 402 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗪𝗵𝗮𝘁 𝗮𝗿𝗲 𝗢𝗔𝘂𝘁𝗵 𝟮.𝟬, 𝗢𝗽𝗲𝗻 𝗜𝗗 𝗖𝗼𝗻𝗻𝗲𝗰𝘁, 𝗝𝗦𝗢𝗡 𝗪𝗲𝗯 𝘁𝗼𝗸𝗲𝗻𝘀, 𝗮𝗻𝗱 𝗦𝗔𝗠𝗟?

When attempting to explain various authorization and authentication standards to their peers or management, such as OAuth, OpenID Connect, and SAML, many professionals in the field face difficulties. This is not to say that they don't understand the concepts or how they're used, but because these protocols are so similar to one, they might be confusing to someone who is trying to learn about. And all of this is usually called Identity and Access Management (IAM).

First, we have some kind of 𝗿𝗲𝘀𝗼𝘂𝗿𝗰𝗲 𝗶𝗻 𝗼𝘂𝗿 𝘀𝘆𝘀𝘁𝗲𝗺 (app, API, etc.) and we have someone who needs to access that resource (this is called identity). That someone can be a user or some other software. 

Second, we also need to understand 𝘄𝗵𝗮𝘁 𝗶𝘀 𝗮𝘂𝘁𝗵𝗲𝗻𝘁𝗶𝗰𝗮𝘁𝗶𝗼𝗻 𝗮𝗻𝗱 𝘄𝗵𝗮𝘁 𝗶𝘀 𝗮𝗻 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗮𝘁𝗶𝗼𝗻. With authentication, we verify that identity who needs to access our resource, if they are who they claim to be and with authorization, we determine what resources that identity can access. 

So, IAM solutions allow us to 𝗰𝗼𝗻𝘁𝗿𝗼𝗹 𝗶𝗱𝗲𝗻𝘁𝗶𝘁𝘆 𝘃𝗮𝗹𝗶𝗱𝗮𝘁𝗶𝗼𝗻 𝗮𝗻𝗱 𝗿𝗲𝘀𝗼𝘂𝗿𝗰𝗲 𝗮𝗰𝗰𝗲𝘀𝘀 𝘁𝗼𝗼. They define which user information to store, but also how users need to prove their identity. Identity providers create and maintain user identity information and they can provide that information to other applications. Examples of identity providers are Microsoft AD and Twitter. 

There are different standards which exists, such as:

• 𝗢𝗔𝘂𝘁𝗵 𝟮.𝟬: is an industry-standard that apps use to grant access to client applications. It is commonly used as a way for users to grant websites access to their information on other websites but without giving them the passwords. It is used by Amazon, Google, and Microsoft to permit users to share info about their accounts with 3rd party apps.

• 𝗢𝗽𝗲𝗻 𝗜𝗗 𝗖𝗼𝗻𝗻𝗲𝗰𝘁: is a layer on top of OAuth and it adds an extra layer of security by encrypting the connection between the user and the app or site. We can use it to enable single sign-on (SSO) between applications by using a security token (ID token).

• 𝗝𝗦𝗢𝗡 𝗪𝗲𝗯 𝘁𝗼𝗸𝗲𝗻𝘀: is an open standard used to share security information between two parties \- a client and a server in JSON format. JWT is sent in the HTTP request with a digital signature. It can be signed using a secret or a public/private key pair.

• 𝗦𝗔𝗠𝗟: is an open standard where authorization and authentication information is exchanged between a service provider and an identity provider (in XML format). It is created in 2002., so it's one of the oldest protocols existing today.

In the image you can see G2 Grid for IAM. 

Check the link in the comments.

\#softwareengineering \#programming \#technology \#security \#techworldwithmilan  
…see more

\=== POST 403 \===  
Hussein Nasser  
View Hussein Nasser’s profile  
   
• 3rd+  
Software Engineer | Talks about backend, databases and operating systems

3yr •   
3yr Visible to everyone

The networking behind clicking a link

When you click on a hyperlink, your browser loads the link’s content from a remote server and renders it. Behind the scenes much is happening including, connection establishement, session encryption, protocol negotiation, redirection, domain indication and much more.

Here are some of the steps that your browser go through before sending the link. This assumes an https link 

🔗 DNS \- Finds IP behind domain

🔗 TCP \- Connects to the backend 

🔗 TLS \- Encrypts session

🔗 ALPN \- negotiate app protocols

🔗 SNI \- Indicates hostname for certificate 

🔗 CERT \- Verifies the full certificate chain

🔗 HTTP \- Sends HTTP GET request 

Read full medium article where I go in details for each step

https://lnkd.in/en-RDW9j \#networking  
…see more

\=== POST 404 \===  
Hussein Nasser  
View Hussein Nasser’s profile  
   
• 3rd+  
Software Engineer | Talks about backend, databases and operating systems

3yr •   
3yr Visible to everyone

Memcached Architecture

Memcached is an in-memory key-value store originally written in Perl and later rewritten in C. It is popular with companies such as Facebook, Netflix and Wikipedia for its simplicity.

While the word “simple” has lost its meaning when it comes to describing software, I think Memcached is one of the few remaining software that is truly simple. Memcached doesn’t try to have fancy features like persistence or rich data types. Even the distributed cache is the responsibility of the client not Memcached server.

Memcached backend has one job only, an in-memory key value store.

In this article I’d like to do a deep dive into the architecture of Memcached and how the devs fought to keep it simple and feature-stripped. I’ll give my opinion on certain components that I believed should have been an option.

I’ll cover the following topics in this article.

\* Memory Management  
\* LRU (Least Recently Used)  
\* Threads  
\* Locking  
\* Read/Writes  
\* Collision  
\* Distributed Cache  
\* Demo

Read full article 

https://lnkd.in/g\_45EJez  
…see more

\=== POST 405 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗪𝗵𝗮𝘁 𝗶𝘀 𝗖𝗗𝗡?

Have you ever wondered how Netflix is so fast when streaming a movie to your house? There is one component that has much importance here and it is called 𝗖𝗗𝗡 (𝗖𝗼𝗻𝘁𝗲𝗻𝘁 𝗗𝗲𝗹𝗶𝘃𝗲𝗿𝘆 𝗡𝗲𝘁𝘄𝗼𝗿𝗸). It is a network of servers that move data fast through the network by using cache servers, as well as edge servers in 𝗣𝗼𝗶𝗻𝘁𝘀 𝗼𝗳 𝗣𝗿𝗲𝘀𝗲𝗻𝗰𝗲 (𝗣𝗢𝗣) 𝗹𝗼𝗰𝗮𝘁𝗶𝗼𝗻𝘀, that are geographically close to the user. Static content of the site (such as videos, images, etc.) is moved to every server on the network. This allows that user connects to the geographically closest server and fetch requested contents from there.

How it works basically, is when a user requests a file using some URL, the DNS routes the request to the best-performing POP location, which is closest to the user. If no servers close to the user have a file in the cache, it is fetched from the origin server. Then, the origin server moves that file to the closest server location (POP). This edge server now caches the file until time-to-live (TTL) specified in HTTP header experiences (default is 7 days). 

CDN allows us a few advantages:

𝟭. 𝗥𝗲𝗱𝘂𝗰𝗶𝗻𝗴 𝗽𝗮𝗴𝗲 𝗹𝗼𝗮𝗱 𝘁𝗶𝗺𝗲

We always want to improve our website page loading speeds and here CDN reduces latencies, which makes higher satisfaction rates for users.

𝟮. 𝗥𝗲𝗱𝘂𝗰𝗲𝗱 𝗯𝗮𝗻𝗱𝘄𝗶𝗱𝘁𝗵 𝗰𝗼𝘀𝘁𝘀

A major cost for websites is the consumption of bandwidth for hosting. The amount of data that an origin server must provide can be decreased by CDNs through caching and other optimizations, which lowers hosting costs for website owners.

𝟯. 𝗜𝗻𝗰𝗿𝗲𝗮𝘀𝗶𝗻𝗴 𝗰𝗼𝗻𝘁𝗲𝗻𝘁 𝗮𝘃𝗮𝗶𝗹𝗮𝗯𝗶𝗹𝗶𝘁𝘆

Large volumes of traffic or hardware issues can prevent a website from operating normally. A CDN can manage more traffic and resist hardware failure better than multiple-origin servers because of its distributed architecture.

𝟰. 𝗜𝗺𝗽𝗿𝗼𝘃𝗶𝗻𝗴 𝘄𝗲𝗯𝘀𝗶𝘁𝗲 𝘀𝗲𝗰𝘂𝗿𝗶𝘁𝘆 

DDoS attacks attempt to shut down applications by flooding the website with a large volume of fictitious traffic. By spreading the load across several intermediary servers, CDNs can manage such traffic spikes while lessening the impact on the origin server.

There are different CDN providers to choose from, such as 𝗦𝘁𝗮𝗰𝗸𝗣𝗮𝘁𝗵, 𝗔𝗸𝗮𝗺𝗮𝗶, 𝗦𝘂𝗰𝘂𝗿𝗶, and 𝗖𝗹𝗼𝘂𝗱𝗳𝗹𝗮𝗿𝗲 (a free one), as well as CDN-s on public cloud providers, 𝗔𝗺𝗮𝘇𝗼𝗻 𝗖𝗹𝗼𝘂𝗱𝗙𝗿𝗼𝗻𝘁 and 𝗔𝘇𝘂𝗿𝗲 𝗖𝗗𝗡.

\_\_\_\_\_\_\_  
If you like my posts please follow me Dr. Milan Milanović and hit the 🔔 on my profile to get a notification for all my new posts.

Grow with me 🚀\!

\#programming \#softwareengineering \#techworldwithmilan \#cloudcomputing \#aws  
…see more

\=== POST 406 \===  
Mohit Sehrawat  
View Mohit Sehrawat’s profile  
   
• 2nd  
DevOps Engineer | Azure, Docker, Kubernetes, Linux, Python | Full-Stack Background (React.js, MERN) | 85K+ LinkedIn Community

3yr •   
3yr Visible to everyone

Are you looking to work Remotely?

Here is a list of companies around the Globe that are remote friendly.

If you find it useful, give it a like and save it.

Also share it with your friends and colleagues out there.

Follow Mohit Sehrawat for more. 

Let's connect: mohitsehrawat.bio.link

𝐇𝐚𝐬𝐡𝐭𝐚𝐠𝐬:  
\#work \#remote \#corporate \#companies \#hiring \#coding \#datastructures \#algorithm \#programming \#webdevelopment \#softwareengineer \#remotejob \#hiringalert \#share   
…see more

Remote Friendly Companies

\=== POST 407 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗪𝗵𝘆 𝗱𝗼 𝘄𝗲 𝗻𝗲𝗲𝗱 𝗧-𝘀𝗵𝗮𝗽𝗲𝗱 𝗱𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿𝘀?

Today we have different kinds of developers, frontend, backend, mobile, and others. They are more or fewer specialists in one field in software engineering. Those engineers are usually experts in their field and they are very productive. However, in today's world of cross-platform teams, this is usually not enough, because a specialist is very focused on only one field of knowledge. 

What we need is a 𝗧-𝘀𝗵𝗮𝗽𝗲𝗱 𝗱𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿. And this means that this person is someone who has a general knowledge of different fields in software engineering (thick horizontal line), but a deeper knowledge in one or more fields (deep vertical line), making this T-shape a developer skillset. These kinds of developers are 𝗯𝗲𝘁𝘁𝗲𝗿 𝗿𝗼𝘂𝗻𝗱𝗲𝗱 𝗮𝘀 𝘁𝗵𝗲𝘆 𝗮𝗿𝗲 𝗰𝗼𝗺𝗳𝗼𝗿𝘁𝗮𝗯𝗹𝗲 𝗱𝗼𝗶𝗻𝗴 𝗼𝘁𝗵𝗲𝗿 𝗷𝗼𝗯𝘀 𝗼𝘂𝘁𝘀𝗶𝗱𝗲 𝘁𝗵𝗲𝗶𝗿 𝗽𝗿𝗶𝗺𝗮𝗿𝘆 𝗮𝗿𝗲𝗮 𝗼𝗳 𝗲𝘅𝗽𝗲𝗿𝘁𝗶𝘀𝗲. They also can help in different tasks and better understand the complete software development lifecycle (SDLC), as well as other developers.

So, how you can become a T-shaped developer:

𝟭. 𝗧𝗿𝘆 𝘁𝗼 𝗹𝗲𝗮𝗿𝗻 𝘁𝗵𝗶𝗻𝗴𝘀 𝗼𝘂𝘁𝘀𝗶𝗱𝗲 𝗼𝗳 𝘆𝗼𝘂𝗿 𝘀𝗽𝗲𝗰𝗶𝗮𝗹𝗶𝘇𝗮𝘁𝗶𝗼𝗻

𝟮. 𝗕𝗲 𝗶𝗻𝘃𝗼𝗹𝘃𝗲𝗱 𝗶𝗻 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲 𝗦𝗗𝗟𝗖 

𝟯. 𝗗𝗼 𝗽𝗮𝗶𝗿 𝗽𝗿𝗼𝗴𝗿𝗮𝗺𝗺𝗶𝗻𝗴 𝘄𝗶𝘁𝗵 𝘆𝗼𝘂𝗿 𝗰𝗼𝗹𝗹𝗲𝗮𝗴𝘂𝗲𝘀 𝘄𝗶𝘁𝗵 𝗺𝗼𝗿𝗲 𝗲𝘅𝗽𝗲𝗿𝘁𝗶𝘀𝗲

𝟰. 𝗕𝗲 𝗰𝘂𝗿𝗶𝗼𝘂𝘀 𝗮𝗯𝗼𝘂𝘁 𝘄𝗵𝗮𝘁 𝗼𝘁𝗵𝗲𝗿 𝗽𝗲𝗼𝗽𝗹𝗲 𝗼𝗻 𝘁𝗵𝗲 𝘁𝗲𝗮𝗺 𝗮𝗿𝗲 𝗱𝗼𝗶𝗻𝗴.

Developers ought to start thinking creatively and being more observant of their surroundings. Teamwork speeds up problem-solving and helps spot emerging problems. Developers gain a new perspective on issue solutions through engaging in conversation, listening to others, and working with individuals from varied backgrounds. This makes 𝗧-𝘀𝗵𝗮𝗽𝗲 𝗱𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿𝘀 𝘁𝗼 𝗯𝗲𝘁𝘁𝗲𝗿 𝗽𝗼𝘀𝗶𝘁𝗶𝗼𝗻 𝘁𝗵𝗲𝗺𝘀𝗲𝗹𝘃𝗲𝘀 𝘄𝗶𝘁𝗵 𝗰𝘂𝘀𝘁𝗼𝗺𝗲𝗿𝘀 𝗮𝗻𝗱 𝗽𝗲𝗲𝗿𝘀, but also open the doors to some other positions where such knowledge is valuable (think a software architect or a product owner). And in general, they change discussion from "𝘄𝗵𝗼 𝗸𝗻𝗼𝘄𝘀 𝗵𝗼𝘄 𝘁𝗼 𝗱𝗼 𝘁𝗵𝗶𝘀" 𝘁𝗼 "𝘄𝗵𝗮𝘁 𝗻𝗲𝗲𝗱𝘀 𝘁𝗼 𝗯𝗲 𝗱𝗼𝗻𝗲".

Which kind of a developer are you? Specialist or T-Shaped one? 

\_\_\_\_\_\_\_  
If you like my posts please follow me Dr. Milan Milanović and hit the 🔔 on my profile to get a notification for all my new posts.

Learn something new every day 🚀\!

\#softwareengineering \#programming \#techworldwithmilan \#career \#personaldevelopment  
…see more

\=== POST 408 \===  
Dr Milan Milanović  
View Dr Milan Milanović’s profile  
   
• 2nd  
Chief Roadblock Remover and Learning Enabler | Helping 400K+ engineers and leaders grow through better software, teams & careers | Author | Leadership & Career Coach

3yr •   
3yr Visible to everyone

𝗪𝗵𝗮𝘁 𝗶𝘀 𝗖𝗿𝗼𝘀𝘀-𝗢𝗿𝗶𝗴𝗶𝗻 𝗥𝗲𝘀𝗼𝘂𝗿𝗰𝗲 𝗦𝗵𝗮𝗿𝗶𝗻𝗴 (𝗖𝗢𝗥𝗦)?

Browsers use CORS, a method, to prevent websites from requesting data from different URLs. A request from a browser includes an origin header in the request message. The browser allows it if it gets to the server of the exact origin; if not, the browser blocks it.

We can deal with CORS issues on the backend. Cross-origin requests require that the values for origin and 𝗔𝗰𝗰𝗲𝘀𝘀-𝗖𝗼𝗻𝘁𝗿𝗼𝗹-𝗔𝗹𝗹𝗼𝘄-𝗢𝗿𝗶𝗴𝗶𝗻 in the response headers match and it is set by the server. When you add an origin to the backend code, the CORS middleware only permits this URL to communicate with other origins and utilize it for cross-origin resource requests.

There are two ways to fix CORS issues:

𝟭. 𝗖𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗲 𝘁𝗵𝗲 𝗕𝗮𝗰𝗸𝗲𝗻𝗱 𝘁𝗼 𝗔𝗹𝗹𝗼𝘄 𝗖𝗢𝗥𝗦

Server can let all domains with 𝗔𝗰𝗰𝗲𝘀𝘀-𝗖𝗼𝗻𝘁𝗿𝗼𝗹-𝗔𝗹𝗹𝗼𝘄-𝗢𝗿𝗶𝗴𝗶𝗻: \*. This actually turns off same-origin policy, which is not recommended. Another optin would be only to allow particular domain, which is better option, e.g., 𝗔𝗰𝗰𝗲𝘀𝘀-𝗖𝗼𝗻𝘁𝗿𝗼𝗹-𝗔𝗹𝗹𝗼𝘄-𝗢𝗿𝗶𝗴𝗶𝗻: 𝗵𝘁𝘁𝗽𝘀://𝘀𝗼𝗺𝗲𝗱𝗼𝗺𝗮𝗶𝗻.𝗰𝗼𝗺.

𝟮. 𝗨𝘀𝗲 𝗮 𝗣𝗿𝗼𝘅𝘆 𝗦𝗲𝗿𝘃𝗲𝗿

We can use a proxy server to call external API. It acts as a middleware between client and the server. If server doesn't return proper headers defined by CORS, we can add then in the proxy.

\_\_\_\_\_\_\_  
If you like my posts please follow me Dr. Milan Milanović and hit the 🔔 on my profile to get a notification for all my new posts.

Learn something new every day 🚀\!

\#softwareengineering \#programming \#api \#apidesign \#techworldwithmilan  
…see more

\=== POST 409 \===  
Nitesh Yadav  
View Nitesh Yadav’s profile  
   
• 2nd  
SWE @Meta l Ex-Amazon | doing some tech stuff

3yr •   
3yr Visible to everyone

Every developer should learn System Design.

List of Design Patterns and System Design resources:

📌 Java Design Patterns: https://lnkd.in/ef73MVzs  
📌 System Design Primer: https://lnkd.in/enzDwNdC  
📌 Awesome Scalability: https://lnkd.in/est63PRt  
📌 Python Patterns: https://lnkd.in/eU-rRX4J  
📌 Design Patterns for Humans: https://lnkd.in/eCbNHDDw  
📌 Design Patterns PHP: https://lnkd.in/eNwEirpS  
📌 Go Patterns: https://lnkd.in/ez\_qdw\_P  
📌 Awesome Design Patterns: https://lnkd.in/eG\_Vwz\_b  
📌 Modular Monolith with TDD: https://lnkd.in/epDd6euz  
📌 Domain Driven Hexagon: https://lnkd.in/eprFDbTi  
📌 Design Patterns in Typescript: https://lnkd.in/e4GXTfW8  
📌 System Design Interview: https://lnkd.in/emWVHshE  
📌 System Design: https://lnkd.in/e9ZvVkbN  
📌 Machine Learning Systems Design: https://lnkd.in/esPSskvR

Let's connect: https://lnkd.in/dauDV9nQ

\#design \#computerprogramming \#technology \#scalability \#developer   
…see more

\=== POST 410 \===  
Vasanth Bhat  
View Vasanth Bhat’s profile  
   
• 2nd  
60K+ Followers on LinkedIn | Speaks about frontend and interview preparation |Staff Software Engineer at Walmart Global Tech India | DM for mentorship \- \+91 97310 39408 (whatsapp)

3yr •   
3yr Visible to everyone

\#interview \#skills there is an overrated interview skill called "think out loud". To start off, I don't use it and you also need not to use it.

1\. Just by talking about something while solving DSA or while doing machine coding you won't get the interviewer's full attention. 

2\. Think in your mind and talk sensible whenever required. Ex: once you're sure about DSA logic explain it to the interviewer, rather shouting something every second.

3\. Most \#interviewer including me will have no \#interest in hearing to \#unclear thoughts that you're talking about. 

4\. By talking every second you even lose a chance to get interviewers attention on \#important point that you're talking about. 

If you wish to think out loud in the interview then think properly before talking, talk only that is sensible. 

Open to hear you thoughts too, mention it in the comment section.

In case if you have not followed me, you can do it here, I will help you to clear your Software developer interview : Vasanth Bhat  
Link to my youtube and telegram channel is in the comment section.

\#interview \#coding \#interviewtips \#interviewtricks \#interviewquestions \#interviewpreparation \#interviewskills \#interviewquestionsandanswers   
…see more

\=== POST 411 \===  
Status is reachable  
Sumit Bhanushali  
View Sumit Bhanushali’s profile  
   
• 1st  
Lead Engineer (SDE-3) @SprintMoney | Ex-Frappe | Ex-Servify

3yr •   
3yr Visible to everyone

API Gateway is one of the key components while designing a microservice architecture. It acts as an intermediary between client and servers. But is it the only thing it can do?

Typically, when an API Gateway receives a request, it parses and validates attributes in the HTTP request and after passing basic checks, the API gateway finds the relevant service to route to by path matching and uses that same connection to respond back to the client.

But there are more things that can be implemented on an API Gateway:

• Authenticating users by routing request to authentication service to verify credentials   
• Validating IP extracted from request by scanning in allow/deny list and perform actions accordingly  
• Checking for valid protocol and API specific parameters validation  
• Rate limiting to prevent DDoS attacks and also to cap requests per user  
• Caching frequently accessed static data with TTL to reduce network hops and reduce load on server  
• Circuit breaking to prevent cascading failures and hence improving response times by adding a threshold to failing microservice for a defined time and responding in error immediately instead of waiting for response  
• Balancing load on servers by adding load balancing algorithms which then can route the request to right server  
• Request Response loggers which can eventually be uploaded to log management service and perform analytics respectively  
• Monitoring health of servers by measuring vitals like CPU, RAM and Storage

\#systemdesign \#architecture \#softwaredevelopment  
…see more

\=== POST 412 \===  
Riti Nema  
View Riti Nema’s profile  
   
• 2nd  
SDE @Atlassian | 100k+ @Linkedin | 2.7k+ @Medium | SpeedCuber | Speaker | Mentor (Top 0.1%) @ Topmate

3yr •   
3yr Visible to everyone

Hello everyone,

Resharing all my interview experiences I have published till now. 

𝗔𝘁𝗹𝗮𝘀𝘀𝗶𝗮𝗻 (17k+ views) : https://lnkd.in/gU7PJy54

𝗚𝗼𝗼𝗴𝗹𝗲 (6k+ views) : https://lnkd.in/d\_ujJyGG

𝗩𝗠𝘄𝗮𝗿𝗲 (4K+ views) : https://lnkd.in/dewRx3eV

𝗚𝗿𝗼𝘄𝘄 (4K+ views) : https://lnkd.in/d3p-RsZm

🔹𝗙𝗼𝗹𝗹𝗼𝘄 me on 𝗠𝗲𝗱𝗶𝘂𝗺 if you find the content helpful. Will be publishing more content in the upcoming days.   
For More: https://lnkd.in/dBaP75J6

 \#interview \#experience \#google \#atlassian \#vmware \#placements \#interviewpreparation \#faang \#softwaredeveloper \#mediumwriters \#medium \#content \#india \#careers \#startups   
…see more

\=== POST 413 \===  
Deepika Dande  
View Deepika Dande’s profile  
   
• 2nd  
SDE-2 @Amazon | Ex- {PayTM-SWE, Amazon-Intern} | Competitive Programmer | CS \- ’21 | Writes to 69k+

3yr •   
3yr Visible to everyone

As this is the time of layoffs, it is a good time to prepare to get the job immediately after the hiring freezes resume.

Sharing my Amazon FTE (Full time) interview experience. I hope it might help.

Amazon hires mostly based on logical thinking and problem solving. The questions that will be asked in the DSA rounds will be purely dependent on interviewers. They make/choose the questions.

There were 5 rounds (For few there might be 4, The last 2 rounds will be compressed to one round).

1\. Online Assessments  
2\. Data Structures and Algorithms (Easy \- Medium)   
3\. Data Structures and Algorithms (Medium \- Hard)  
4\. Managerial Round  
5\. Bar Raiser

Online Assessments:  
This will be easy among all the rounds. As companies don't want to reject the candidates in very first basic phone interviews or online assessments. They always try to interact with the candidate in depth. 

For me it had 2 DSA questions (Easy \- Medium) and 2 reasoning questions. Reasoning questions are about the DSA questions that you solved in the assessment. You need to provide details about how you approached the problem and what's the time complexity that your code takes.

DSA \- 1 (Easy \- Medium)  
1\. Binary search  
2\. BFS

If you know the solution, explain the brute force first (DO NOT code, it's waste of time) and then jump to optimised solution. Make sure you cover all the edge cases. 

If you don't know, speak what you think. Interviewers will always be there to give minute hints. You should be able to catch them.

DSA \- 2 (Medium \- Hard)  
1\. Maps (Tricky)  
2\. Back tracking 

Managerial round :  
SDM (Software Development Manager) will be your interviewer. There will be questions around the projects that you did, past experiences that you have and most importantly leadership principles. 

Bar raiser round :  
It has similar topics from managerial round and they will also assess your coding skills

1\. They will give you a problem and ask you to code to it. You should be able to code in a way such that the code is readable and maintainable. which means, another person should easily make changes to the code that you wrote.  
2\. In the next step they will give an improvisation challenge. Basically they tweak their question that they asked first and ask you to make changes in the code that you wrote with minimal code changes.

Hope this helps. Make best use of this time. All the best all tiers ❤️

\#datastructures \#complexity \#coding \#softwaredevelopment \#algorithms \#interview \#hiring \#experience \#projects \#leadership \#interviewpreparation \#interviewexperience 

…see more

\=== POST 414 \===  
Vivek Gupta  
View Vivek Gupta’s profile  
   
• 1st  
Building AlgoZenith | Ex-Google | ICPC World Finalist | Taught DSA & CP to over 3000+ Students

3yr •   
3yr Visible to everyone

I am planning to switch to Web3 and Blockchain world now\! What resources would you suggest to someone who is changing just now? I will also put my recommendation in the comments, but I look forward to more awesome resources\!\!

\#web3 \#blockchain  
…see more

\=== POST 415 \===  
Status is reachable  
Shivshankar Nagarsoge  
View Shivshankar Nagarsoge’s profile  
   
• 1st  
Tech @ Autodesk | Ex-Intuit, PubMatic | Java Backend Developer | Scalable Systems with Java, Spring Boot & AWS | AI Enthusiast & Emerging Tech Explorer

3yr •   
3yr Visible to everyone

Tips for an impressive LinkedIn Profile \-

Credit \- Coder Rahul

 \#linkedin \#linkedinprofile \#linkedinprofileoptimization   
…see more

Winning LinkedIn Profile

\=== POST 416 \===  
Priya Vajpeyi  
View Priya Vajpeyi’s profile  
   
• 2nd  
Senior Brand Manager @ Extramarks | Building What Lasts Beyond Trends | TedX & Josh Talks Speaker 🎙 | Full-Cycle Brand Management & GTM Strategy | Ex-Adobe & Morgan Stanley 💼

3yr •   
3yr Visible to everyone

If you're laid off/ looking for a switch to some good companies, 𝐡𝐞𝐫𝐞'𝐬 𝐚𝐧 𝐚𝐥𝐩𝐡𝐚𝐛𝐞𝐭𝐢𝐜𝐚𝐥 𝐥𝐢𝐬𝐭 𝐨𝐟 𝐦𝐚𝐧𝐲 𝐟𝐚𝐧𝐭𝐚𝐬𝐭𝐢𝐜 𝐜𝐨𝐦𝐩𝐚𝐧𝐢𝐞𝐬. 

✅ Please re-share the post & save to help all those in needs ❤️

A  
Accolite software  
Accord software  
Adobe  
Able  
Abstract  
Acko  
Accredible  
Agile Solutions  
Agnikul Cosmos  
Airbase  
Airbnb  
Airbus  
Airtel x labs  
Ajio  
Akamai  
Alstom  
Amadeus labs  
Amazon  
Amdocs  
American express  
Amway  
Apna  
App Dynamics  
Appen  
Apple  
AppInventiv  
Aptiv  
Arcesium  
Arista Networks  
Aryaka networks  
Asteria Aerospace Ltd  
Athena Health  
Atlan  
Atlassian  
Avaya  
(back to top)

B  
Barclays  
Bain & Co  
BARC India  
Bazaarvoice  
Bellatrix Aerospace  
Benchmark  
Better  
BharatPe  
BigBasket  
BlackBuck  
Blackrock  
Block Inc  
Bloomberg LP  
BlueJeans  
Bluestacks  
BMC software  
BNY Mellon  
Boeing  
Booking.com  
Bosch  
Bottemline Technologies  
Bounce  
Box  
Brahmastra Aerospace  
Browser stack  
BukuWarung  
Byju's  
ByteDance  
(back to top)

C  
Cadence  
Capillary  
Capital One  
CarDekho  
Careem  
CarWale  
Cashfree  
Cimpress  
Celigo  
Cerner  
Chargebee  
Chronus  
Cisco  
Citadel  
Citadel Securities  
Citrix  
Classplus  
ClearGlass  
Cleartrip  
Cloudera  
Codenation innovation labs  
CodingNinjas  
Cognizant  
CoinBase  
CoinDCX  
Coinswitch kuber  
Commvault  
Continental  
Contra  
Coupang  
Cradlepoint  
Cred  
Credit Suisse  
Crestron  
Crowdstrike  
CSS Corp  
cure.fit  
Cvent  
(back to top)

D  
DailyHunt  
Dashlane  
Databricks  
Dataminr  
DBS  
D. E. Shaw & Co.  
DealShare  
Delhivery  
Dell  
Deutsche Bank  
Dhruva Space  
Dialpad  
Directi  
digit  
Discord  
Discovery inc  
Disney  
DoorDash  
DP World  
DRDO  
Dream11  
droom  
Dropbox  
Druva  
Dukaan  
Dunzo  
DuPont  
(back to top)

E  
EA Games  
Enfussion  
Envestnet Yoodlee  
Ericsson  
Eurofins  
EXL Healthcare  
Expedia  
EY  
EyeROV  
(back to top)

F  
F5  
factset  
FamPay  
Fidelity investments  
FireEye inc  
Fischer Jordan  
fiserv  
Flexport  
Flipkart  
FlyFin  
Fractal  
Frappe Technologies  
FreeCharge  
Freshworks  
Furlenco  
fyle  
Fico  
(back to top)

G  
Gartner  
Garuda Aerospace private Ltd  
GeeksForGeeks  
GE  
GE Healthcare  
Ghost  
Github  
Gitlab  
GoDaddy  
GoDigit  
Godrej Aerospace  
Gojek  
Goldman Sachs  
Google  
Global Logic  
Grab  
Gravitont Rading  
Groupon  
Grofers  
Groww  
(back to top)

H  
Hackerearth  
HackerRank  
Hashedin  
HBO  
HealthAsyst  
Healthify me  
HERE  
Hexagone  
Hotstar  
Honeywell  
HP  
(back to top)

I  
IBM  
IdeaForge  
IHS Markit  
Impact Analytics  
Indeed  
India Mart  
Infor  
Informatica  
Infospoke  
Inmobi  
Innovaccer  
Intel  
Intellika  
Intuit  
IP Infusion  
ISRO  
iQuanti  
(back to top)

J  
Jaguar  
Jio  
JM Financial  
JP Morgan  
Juniper networks  
Jupiter money  
Juspay  
Jumbotail  
(back to top)

K  
Kantar  
Kesari bharat  
Keyvalue  
Khatabook  
khoros  
KLA Tencor  
Koch  
(back to top)

L  
Land rover  
Lenskart  
Leap Finance  
Licious  
LinkedIn  
LogicFruit  
Logicmonitor  
Lowe's companies, inc  
(back to top)

M  
Magicpin  
MakeMyTrip  
Mastercard  
Mastery  
Mathworks  
McKinsey  
Media.net  
Meta  
Meesho  
Memory  
Micron  
Microsoft  
MindTickle  
MobiKwik  
Morgan Stanley  
Mount talent  
MPL  
MTX  
Myntra  
(back to top)

Follow Priya Vajpeyi for more\!  
…see more

\=== POST 417 \===  
Chinmay Chaudhary  
View Chinmay Chaudhary’s profile  
   
• 2nd  
VP, Product Engineering at Sprinklr

3yr •   
3yr Visible to everyone

We, at Sprinklr, are looking for enthusiastic frontend engineers. If you resonate with the following, share your resumes with mansi.bhayana@sprinklr.com ( Mansi Bhayana ) :  
1\. Leveraging the power of JavaScript, HTML, and CSS to develop neat user experiences across devices  
2\. Learning the rendering patterns ( https://lnkd.in/eU8FAqiJ )  
3\. Diving deep into the fundamentals to improve page load performance ( https://lnkd.in/evHmSYXM )  
4\. Getting a stronghold of the basic React concepts ( https://beta.reactjs.org/ )  
5\. Learning about CDN, cloud storage, typescript, graphql & basic CSS transitions  
6\. Learning about how content management systems, consent management platforms, tag managers & third-party scripts work

Feel free to share the opportunity with your friends and family.

Location: Gurgaon & Bangalore  
Experience: 1-4 years

\#hiring \#frontendhiring \#frontend \#softwareengineer \#seniorsoftwareengineer \#frontendengineer \#seniorfrontendengineer \#frontenddeveloper \#seniorfrontenddeveloper \#reactdeveloper \#reactjobs   
…see more

\=== POST 418 \===  
Arnav Gupta  
View Arnav Gupta’s profile  
   
• 2nd  
Infra @ Meta | Consumer Internet, Mobile Apps & EdTech | Ex: Viacom, Zomato, Target & startups

3yr •   
3yr Visible to everyone

Are you a 'senior' software engineer? What does SDE1, SDE2, SDE3 mean? Should you apply for a position for a lead engineer? 

Given that I interact with a lot of engineers starting out their careers, as well as some mid-senior engineers on a daily basis, I realise not a lot of people actually understand what really are these "levels" in software engineering. (Hint: It is not just how many years you are experienced). 

Some good websites from where it is possible to understand what are the expectations from a different seniority of software engineers (also engineering managers) are these \- 

\- progression\[.\]fyi : they list career progression frameworks of many well known tech companies 

\- engineeringladders\[.\]com : very nice description of expectations along tech, system, process, people skills needed at each level for each role 

\- career-ladders\[.\]dev : more simplistic description of what engineers should do at each level.

If you are in large and well established tech company you'll most likely have some internal portal where such a framework is available which would give you better idea on what parameters your manager evaluates you at your current level. Unfortunately for people in startups and smaller/younger companies do not always have such a well-established levelling system internally, but the industry-wide expectations are anyway still the same. 

You'll only be able to progress in your career if you truly understand what is expected out of someone at the next level. 

One advise \- remember as you go up, importance of understanding "people" becomes more important than understanding "code". And understanding how the "team" works is just as important as understanding how the "system" works.   
…see more

\=== POST 419 \===  
Arslan Ahmad  
View Arslan Ahmad’s profile  
   
• 2nd  
Author of Bestselling ‘Grokking’ Series on System Design, Software Architecture & Coding Patterns | Founder DesignGurus.io

3yr •   
3yr Visible to everyone

𝗦𝗼𝗺𝗲 𝗼𝗳 𝗺𝘆 𝗳𝗮𝘃𝗼𝗿𝗶𝘁𝗲 𝘀𝗼𝗳𝘁𝘄𝗮𝗿𝗲 𝗮𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲 𝗮𝗻𝗱 𝘀𝘆𝘀𝘁𝗲𝗺 𝗱𝗲𝘀𝗶𝗴𝗻 𝗿𝗲𝘀𝗼𝘂𝗿𝗰𝗲𝘀

It takes time and effort to learn software architecture and system design. I've learned a lot from the following resources: 

1\. 𝗗𝗮𝘁𝗮 𝗘𝗻𝗴𝗶𝗻𝗲𝗲𝗿𝗶𝗻𝗴: Designing Data-Intensive Applications, Martin Kleppmann \- https://lnkd.in/gGk6Kric

2\. 𝗦𝘆𝘀𝘁𝗲𝗺 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲: Clean Architecture, Robert C. Martin \- https://lnkd.in/gj4NdZaC?

3\. 𝗗𝗼𝗺𝗮𝗶𝗻-𝗗𝗿𝗶𝘃𝗲𝗻 𝗗𝗲𝘀𝗶𝗴𝗻: Domain-Driven Design: Tackling Complexity in the Heart of Software, Eric Evans \- https://lnkd.in/gRfKxGFY

4\. 𝗠𝗶𝗰𝗿𝗼𝘀𝗲𝗿𝘃𝗶𝗰𝗲𝘀: Building Microservices: Designing Fine-Grained Systems, 2nd Edition, Sam Newman \- https://lnkd.in/dZKf7fgQ

5\. 𝗦𝘆𝘀𝘁𝗲𝗺 𝗗𝗲𝘀𝗶𝗴𝗻: Grokking the Advanced System Design Interview, Design Gurus \- https://lnkd.in/dyCRtiec

6\. 𝗖𝗹𝗼𝘂𝗱 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲: Cloud Architecture Patterns: Using Microsoft Azure, Bill Wilder \- https://lnkd.in/gFmCFh5h

7\. 𝗠𝗶𝗰𝗿𝗼𝘀𝗲𝗿𝘃𝗶𝗰𝗲𝘀: Monolith to Microservices: Evolutionary Patterns to Transform Your Monolith, Sam Newman \- https://lnkd.in/gb3txbKp  
   
8\. 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗮𝗻𝗱 𝗠𝗲𝘀𝘀𝗮𝗴𝗶𝗻𝗴: Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions, Gregor Hohpe, Bobby Woolf \- https://lnkd.in/dtey2KXc

9\. 𝗗𝗶𝘀𝘁𝗿𝗶𝗯𝘂𝘁𝗲𝗱 𝗦𝘆𝘀𝘁𝗲𝗺𝘀: Designing Distributed Systems: Patterns and Paradigms for Scalable, Reliable Services, Brendan Burns \- https://lnkd.in/ds4nu8St

10\. 𝗪𝗲𝗯 𝗦𝗰𝗮𝗹𝗮𝗯𝗶𝗹𝗶𝘁𝘆: The Art of Scalability: Scalable Web Architecture, Processes, and Organizations for the Modern Enterprise, 2nd Edition, Martin Abbott, Michael Fisher \- https://lnkd.in/gzvW9GBD

\--  
Feel free to follow me for tips on \#systemdesign, \#softwarearchitecture, \#codinginterview, \#interviewtips

Join our \#newsletter for tips on \#coding and system design interviews: https://lnkd.in/gKDjdn9m

\#software \#cloudcomputing \#softwareengineering \#books \#microservices \#interview \#design \#scalability \#learning \#data  
…see more

\=== POST 420 \===  
Kumar Vidit  
View Kumar Vidit’s profile  
   
• 2nd  
Software developer@IBM cloud | ex-Amazon | designing cloud solutions | AWS expert

3yr •   
3yr Visible to everyone

So lets talk about how I managed to prepare DSA with my full time job. 

In my opinion for making a schedule that turns out to be perfect, you need to keep in mind the following points. 

🖍️. list your priorities first so at the end of the day you don't feel like " aaj kuch bhi ni kia". 

🖍️. don't priorities what you would like to do, rather do what is best for your short term goal. 

🖍️. Don't pick too many things in your bucket. Remember sb kuch step by step hota h ek din me nahi. 

🖍️. If you have X thing scheduled at 4am to 5am do it daily at that time only. ye nahi ki workout toh krna h kabhi sham me krlia kabhi subha. 

🖍️. fix your total sleeping hours. for me it was 6 hours and that too 4hrs at night and 2 hrs in daytime.

So here is a plan I made for me-----------x

my priorities were in order   
1\. DSA practice  
2\. company work  
3\. my personal work  
4\. sleep time 

my schedule-  
📝 6-10am (4hours)  
 DSA prep.

📝 10-10:30am (30 mins)   
 eat something

📝 10:30-12:30pm (2 hours)   
 sleep 😴

📝 12:30-1:30pm (1hour)   
 bath, lunch time

📝 1:30-9:30 (8 hours)  
 my company work

📝 9:30- 10:30 (1 hour)   
 dinner and break.

📝 10:30- 12 (1.5hour)  
 DSA prep

📝 12- 2 (2 hours)  
 personal time aur phone me time   
 khrab krna 

📝 2-6 am (4 hours)  
 sleep 😴 

bonus \- "koi bhi insaan schedule ko 100% follow nahi kr skta daily for many reasons, so don't blame yourself agr aap bhi nahi kr paate follow. All you should aim for is, try your best to follow it". 

follow for more tips and strategies.

\#amazon \#dsa \#schedule  
…see more

\=== POST 421 \===  
Touseef Liaqat  
View Touseef Liaqat’s profile  
   
• 1st  
Engineering Leader | Building AI at Microsoft | 2x Founder | Ex-Meta, Ex-Airbnb | | Startup Advisor/Mentor

3yr •   
3yr Visible to everyone

7 best videos on system design.   
   
   
Watch these videos and jump start in system design interview prep. I recommend watching each video multiple times.   
   
Scalability Harvard Web Development • David J. Malan   
https://lnkd.in/gPh4e6gz   
   
Distributed Systems in One Lesson • Tim Berglund   
https://lnkd.in/gA9PGbgW   
   
Building Scalable, Highly Concurrent and Fault-Tolerant Systems • Jonas Bonér   
https://lnkd.in/gNJgwR6r   
   
Four Distributed Systems Architectural Patterns • Tim Berglund   
https://lnkd.in/gPBZ6jPj   
   
Microservices • Martin Fowler  
https://lnkd.in/gUfVVf2N   
   
What I Wish I Had Known Before Scaling Uber to 1000 Services • Matt Ranney   
https://lnkd.in/gJR-tYtH   
   
Event-Driven Architectures Done Right, Apache Kafka • Tim Berglund  
https://lnkd.in/gjhpiFxX   
   
\#distributedsystems \#\#systemdesign \#interviews \#microservices \#scalability \#systemarchitecture  
…see more

\=== POST 422 \===  
Abhimanyu Saxena  
View Abhimanyu Saxena’s profile  
   
• 2nd  
Co-Founder at InterviewBit and Scaler

3yr •   
3yr Visible to everyone

Given a chance to have an hour long meeting with CEO of Disney, most would travel a thousand mile for that, but how many read the books written by him?   
Three books which I felt gave me as much insights as spending hours with the author, and helped me learn and get better as a founder are:

\- Zero To One by Peter Thiel

No matter what stage of business or entrepreneurship you are at, this book will change they way you think or approach things.

\- \*\*The Hard Thing About Hard Things by Ben Horowitz\*\*

Most Founders don’t know how to prepare for the hard times. This book will show you unpredictable situations you may find yourself in, and some tips on how to manoeuvre around them.

\- Atomic Habits by James Clear

Successful people are simply those with successful habits, said Brian Tracy. If you also believe habits form you \- you need this book.

Which book will you recommend? Comment below\!  
…see more

\=== POST 423 \===  
Pratima Upadhyay  
View Pratima Upadhyay’s profile  
   
• 2nd  
Engineering at Airbnb | Women in Tech Mentor | Distributed Systems | Software Engineering | System design | Data structures | Algorithms

3yr •   
3yr Visible to everyone

I have received a lot of messages from folks who want to understand the interview process at Airbnb and the compensation details.  
While I cannot share the actual questions that were asked in the interview, I'll try to outline the number of rounds and the topics which were asked in each round.  
   
1\. First round was screening which was an online assessment test. This round had a single problem on trees. It's difficulty level was LC-Hard  
   
2\. The screening was followed by 2 live coding rounds. Here, you were expected to come up with a working solution for the given problem in 45 mins. These were elimination rounds and the difficulty level of the questions was LC- Medium. The questions were scenario based.  
   
3\. Fourth round was a design round which mainly focused on High Level Design. Here you were expected to come up with the API design and DB schema of the presented problem.  
   
4\. Fifth round was a technical experience round. Here you need to present any one of your projects that you had worked on and go through the major design decisions that you had to take, what went well and what were the scope of improvements. Design and Technical experience were also elimination rounds.  
   
5\. Post this there were 2 Cultural fit rounds.  
   
Overall, there were a total of 7 rounds which consisted of 3 sets of eliminations.  
   
For compensation details, you can refer to posts on leetcode.  
eg https://lnkd.in/gwjJ2mRD

For coding rounds, I would suggest practice the concepts thoroughly on leetcode or any other platform you're comfortable with.   
Master recursion, backtracking, dynamic programming, graphs, hashmaps and trees. Keep practicing\! 

 \#coding \#programming \#interview \#experience \#codinginterview \#interviewexperience \#designinterview \#recursion \#trees \#graphs \#dp \#airbnb \#bigtech \#faang \#faangmula \#softwaredesign \#networking \#computerprogramming \#softwarearchitecture \#softwareengineer \#socialmedia \#computerscience \#socialnetworking \#India \#Innovation \#HumanResources \#DigitalMarketing \#Technology \#leanstartup \#professionalwomen \#computersoftware \#womenengineers \#womanintech \#womenintechnology \#engineeringjobs  
…see more

\=== POST 424 \===  
Arslan Ahmad  
View Arslan Ahmad’s profile  
   
• 2nd  
Author of Bestselling ‘Grokking’ Series on System Design, Software Architecture & Coding Patterns | Founder DesignGurus.io

3yr •   
3yr Visible to everyone

Google Interview Guide (2022)  
\---

Interview Process  
\---  
What to expect in a Google interview:  
   
\* Recruiter Pre-screen (20-30 mins) – Non-technical chat about your resume and background. Get ready to answer questions like Why Google? Why are you leaving your current job? What's your biggest achievement? 

\* Technical Phone Screens (45-60 mins) – One or two phone screens with your hiring manager or a Google employee. You'll solve a coding question related to data structures and algorithms on a shared Google Doc. Some questions on your background.

\* Onsite Loop (4-5 interviews) – Coding and System Design questions. Expect questions related to slightly harder data structure, algorithms, and system design. 

Google evaluates candidates on 4 criteria:  
   
1\) Googleyness  
Googleyness means putting the user first, being friendly, approachable, humble, doing something nice for others, being proactive, and keeping your eye on the goal. You'll be gauged for being a team player and having a bias for action.

2\) General Cognitive Ability  
Your ability to solve problems and explain your thought process. Expect open-ended questions like how would you optimize this further? The interviewer wants to know how you learn and adapt to a situation.  
​  
3\) Leadership  
Your ability to take on tough problems and step back when it's not needed. They'll gauge if you can mobilize a team to solve a difficult problem. Get ready to answer questions like, how have you demonstrated leadership when you weren't the manager? how have you dealt with trade-offs and ambiguity?  
​  
4\) Role-related knowledge  
Is your technical expertise sufficient to drive impact at Google? How will you grow and scale with the company? Sample questions: Tell me about a recent/interesting project you worked on? How would you design a task scheduling system?  
 

Interview Tips  
\---  
\* Data Structures \- Practice data structures like Heaps, HashTable, Tree, Stack, Queue, Graph, and Trie.   
\* Algorithm \- Practice Dynamic Programming, Quick-Sort, Breadth-first and Depth-first search.  
\* Explain your thought process \- Extremely important. Practice describing your design decisions clearly and concisely.  
\* Collaborate – Don't forget to discuss tradeoffs, present multiple solutions, and take hints from the interviewer.

Top recent Google tagged Coding Questions on LeetCode  
 \---  
Happy Number (easy)  
Minimum Meeting Rooms (medium)  
Number of Islands (medium)  
Merge Intervals (medium)  
Number of Closed Islands (medium)  
Making a Large Island (hard)  
Employee Free Time (hard)  
Alien Dictionary (hard)

   
Top Google System Design Questions  
\---  
Design a Web Crawler  
Design Google Docs  
Design a Messenger  
Design YouTube

Follow: Arslan Ahmad

Ref:  
1\) Grokking the Coding Interview: https://lnkd.in/gkjFsTxa  
2\) Grokking the System Design Interview: https://lnkd.in/g4Wii9r7  
3\) Google Interview Guide: https://lnkd.in/gtUN8qnE

\#google \#sde \#datastructures \#algorithms \#systemdesign \#leetcode \#coding \#codinginterview  
…see more

\=== POST 425 \===  
Ankit Kumar  
View Ankit Kumar’s profile  
   
• 2nd  
AI Product Manager | Startup Founder (Hiron AI, Acquired) | Mentoring Engineers in Product & AI Innovation

3yr •   
3yr Visible to everyone

Googleyness & Leadership Interview || Google 

Googleyness is a trait that Google looks for in all the candidates they interview. As Google says it, it is what the Googlers make it. To ensure the candidate is a right fit for the culture, candidates may undergo a G\&L interview.

Here are some example questions to give you an idea of the G\&L round:

1\) Why do you want to work at Google?

2\) What is your favorite Google product, and how would you improve it?

3\) Tell me about something you’ve done that you’re proud of.

4\) Tell me about a time you helped a team member accomplish their task.

5\) How do you handle a situation when someone you’re working with does not agree with the recommended approach to fulfilling the task?

6\) When was the last time you made a wrong decision?

7\) How do you prioritize your tasks?

8\) Tell me about a time you took leadership in a task you were not expected to.

9\) Tell me about one of the technical challenges you might have faced.

10\) What do you do to gain commitment from your team?

These questions mainly aim to understand your style of working, your work ethic, and your ability to work in teams as a member or as a leader. The best way to prepare for the G\&L round is to follow the STAR method:

S — Talk about the situation at hand  
T — Task(s) or the goal(s) you were working towards  
A — Action taken to address the situation  
R — The result of the action

Content by \- FAANGPath  
Content type \- \#interviewquestions  
Follow: Ankit Kumar

Tags \-  
\#interviews \#leetcode \#questions \#google \#sde \#interviewpreparation \#coding \#computerscience \#softwareengineer \#workforwin \#leadership 

…see more

\=== POST 426 \===  
Vasanth Bhat  
View Vasanth Bhat’s profile  
   
• 2nd  
60K+ Followers on LinkedIn | Speaks about frontend and interview preparation |Staff Software Engineer at Walmart Global Tech India | DM for mentorship \- \+91 97310 39408 (whatsapp)

3yr •   
3yr Visible to everyone

\#wipro \#infosys Recently I'm seeing a lot of inferiority among engineers who work for service companies. They somehow feel people who work for product companies are superior and worship guys who have cleared big product firms like \#atlassian \#uber etc. from a service company. 

Here is what I think:

1\. End of the day everybody is an engineer/graduate whether you work for a product company or service company.

2\. You decide whether you're a typical service company guy who just gets the work done or understand the intrinsics and stand unique. There are many engineers in product companies who have a typical service company mindset and vice versa.

3\. There is a myth that product company engineers learn more than service company engineers. Most of the products get into a maintenance phase after a point and you get new projects in service companies, whereas product company engineers may not have new products right away. Either they end up on the bench or do a boring job of fixing minor bugs.

4\. Some think product companies have higher job security. In this difficult phase of inflation all the major players who fired engineers are from product companies. Big service firms like Infosys, Wipro are actively hiring people and helping a lot of families during difficult times.

5\. If India is becoming a goto place for product companies it's only because of big service firms who hired a lot of engineers and transformed them into better engineers.So, let's be respectful about them. 

If you wish to work for any type of company I'm not against it, but never be inferior about the phase of life that you're into. There are many out there who are dreaming the role that you have but unable to get inside.

In case if you have not followed me, you can do it here, I will help you to clear your frontEnd developer interview : Vasanth Bhat

\#infosys \#wipro \#accenture \#service \#product \#superior \#india \#job \#work  
…see more

\=== POST 427 \===  
Status is reachable  
Nikita Gupta  
View Nikita Gupta’s profile  
   
• 2nd  
Co-Founder @Careerflow.ai | Keynote Speaker | Ex-Senior Technical Recruiter @Uber | Ex @Amazon | 493K+ Followers | TEDx Speaker | Daily AI content about job search tips | YouTuber

3yr •   
3yr Visible to everyone

With so much news about layoffs by companies like Shopify, Coinbase, Oracle, Nutanix, Linktree, LinkedIn,Career Karma, Microsoft, Google, Peloton Interactive and others, I wanted to re-share some tips on how to create an effective LinkedIn profile with everyone here, hoping those affected by the layoffs or looking for jobs can benefit from it. 👇🏻 

As a recruiter, I also use LinkedIn daily to reach out to job seekers via LinkedIn.

An efficient LinkedIn account is your way of building connections, expanding your network, and moving up in your desired field. Unfortunately, although LinkedIn has been the career and networking hub for a long time now, most people still don't understand the importance of this POWERFUL platform.

Some tips on how I got multiple interview calls:

1\. Added keywords to my profile which made my profile pop up in SEO engine of recruiters  
2\. Added "open to work" to my profile  
3\. Updated summary: add at-least 3 paragraphs to share details about yourself  
4\. Took recommendations and endorsements  
5\. Added keywords in the Headline: Add exact title, with hard skills  
6\. Made my profile all-star: Add all the sections from top to bottom  
7\. Added relevant projects specially academic  
8\. Added professional headshot

I made sure everything on my profile was updated to that extend that no one needed to ask me for anything  
Recruiters always appreciate your efforts.

You can also search for hiring managers and recruiters who are hiring actively using our Hiring Search tool \- https://lnkd.in/gieVjzju.

Please share this with your network so more and more people can benefit from it\! Also, reach out to me for any resume or interview guidance.

Let us help more folks get hired 💪  
.  
.  
.  
.  
Follow FAANGPath and me for job search resources\!

\#Workfromhome \#google \#microsoft \#amazon \#apple \#facebook \#jobsearch \#opentowork \#networkingtips \#linkedintips \#networking \#entrepreneurship \#india \#workingathome \#careers \#startups \#interview \#job \#recruitment \#careers \#Socialmedia \#jobinterviews \#openfornewopportunities \#hiringengineers \#softwareengineerjobs \#jobopportunites \#jobseekers \#linkedin \#recruiters \#jobs \#netflix \#hiring \#tech \#career \#marketing \#leadership \#jobsearchresources \#softwareengineer \#coding \#layoffs  
…see more

Search for recruiters and hiring managers of your favourite companies

hiring-search.faangpath.com

\=== POST 428 \===  
Status is reachable  
Nikita Gupta  
View Nikita Gupta’s profile  
   
• 2nd  
Co-Founder @Careerflow.ai | Keynote Speaker | Ex-Senior Technical Recruiter @Uber | Ex @Amazon | 493K+ Followers | TEDx Speaker | Daily AI content about job search tips | YouTuber

3yr •   
3yr Visible to everyone

Want to work abroad or remotely? 🌏

I wanted to share some websites and a list of companies below to help you land a job in the country of your choice\! 🔥

Top 10 websites to find jobs abroad ⛳️

👉🏼 Indeed Worldwide \- https://lnkd.in/g9J898FE  
👉🏼 Easy Expat \- https://www.easyexpat.com/  
👉🏼 Jooble \- https://jooble.org/  
👉🏼 Go Overseas \- https://www.gooverseas.com  
👉🏼 Career Builder International \- https://lnkd.in/g23XiCjU  
👉🏼 CareerJet \- https://www.careerjet.com/  
👉🏼 Overseas Jobs \- https://lnkd.in/gPcfNtZ9  
👉🏼 Go Abroad \- https://jobs.goabroad.com/  
👉🏼 Going Global \- https://www.goinglobal.com  
👉🏼 Monster Worldwide \- https://lnkd.in/gEPzeKKT

If you are looking for companies that can sponsor work visas for you, here are the top 10 companies 💳 

👉🏼 Google  
👉🏼 Amazon  
👉🏼 Microsoft  
👉🏼 Meta  
👉🏼 IBM  
👉🏼 Capgemini  
👉🏼 Deloitte  
👉🏼 McKinsey & Company  
👉🏼 Apple  
👉🏼 PwC

Are you looking for remote work opportunities? Apply through these websites 🔗

👉🏼 ARC \- https://lnkd.in/gzcE\_T3t  
👉🏼 JustRemote \- https://justremote.co/  
👉🏼 Remote.Co \- https://lnkd.in/grcRptcW  
👉🏼 Virtual Vocations \- https://lnkd.in/gRsJ3BAX  
👉🏼 Pangian \- https://pangian.com/  
👉🏼 Remotive \- https://remotive.com/  
👉🏼 Remote OK \- https://remoteok.com/  
👉🏼 Jobspresso \- https://jobspresso.co/  
👉🏼 Outsourcely \- https://lnkd.in/gfYknj\_h  
👉🏼 AngelList \- https://angel.co/

Also, here's a list of companies that allow benefits to work from anywhere 🧑🏼‍💻

👉🏼 Airbnb  
👉🏼 Spotify  
👉🏼 Zillow  
👉🏼 Salesforce  
👉🏼 Reddit, Inc.  
👉🏼 GitLab  
👉🏼 Quora  
👉🏼 American Express  
👉🏼 Atlassian  
👉🏼 Mastercard

If you have been affected by the latest layoffs, I have curated a list of job openings here \- https://lnkd.in/gUMejk99

You can also use our Hiring Search tool to look for hiring professionals with active openings \- https://lnkd.in/gcmGcmyV

Share this list with your network if you found it helpful\! 🤝  
.  
.  
.  
.  
Follow FAANGPath and me for more job search resources\!

\#Workfromhome \#google \#microsoft \#amazon \#apple \#facebook \#jobsearch \#opentowork \#networkingtips \#linkedintips \#networking \#entrepreneurship \#india \#workingathome \#careers \#startups \#interview \#job \#recruitment \#careers \#Socialmedia \#jobinterviews \#openfornewopportunities \#hiringengineers \#softwareengineerjobs \#jobopportunites \#jobseekers \#linkedin \#recruiters \#jobs \#netflix \#hiring \#tech \#career \#marketing \#leadership \#softwareengineer \#coding \#remoteopportunties \#jobsearchresources  
…see more

\=== POST 429 \===  
sukhad anand  
View sukhad anand’s profile  
   
• 2nd  
Senior Software Engineer @Google | Techie007 | Opinions and views I post are my own

3yr •   
3yr Visible to everyone

On 10th July 2022, Canada's internet was DOWN. People were flocking to coffee shops/libraries for internet. I could not get in touch with my friends. How can complete country's internet go down like a house of cards ? Let's dissect it through our technical lenses.

1\. Before we go to the actual technical issue, let's focus on how do we or anyone in the world gets internet ? You get it through some company or what you call ISP \- Internet service providers.

2\. They are a lot of telecom companies providing internet in India including Airtel, Jio, Vodafone, ACT etc. But, in Canada, there are only 3 ISPs which control 90% of Canada's traffic. These are: Rogers, Bell Canada and Telus Corp. 

3\. The issue was with Rogers which alone provides internet to 11 million Canadians. They came out with an apology calling it a maintenance issue. But, we techies don't stop at that.

4\. Cloudflare which monitors internet traffic gave a more detailed analysis, saying that the outage was caused due to a glitch in the Border Gateway Protocol.(BGP)

5\. Before we go to BGP, let's first understand what internet is from its textbook definition. Internet is simply a network of networks. So, you are connected to one of the network which is your ISP's network which is then connected to other networks on which you are able to access information. Now how is this ISP connected to other networks ?

6\. That's when Border Gateway Protocol comes in. BGP allows one network to advertise its presence to other networks which together form the internet. Rogers stopped advertising, so no other network could find its presence and hence no one on Rogers Network could connect to anything on the Internet.

7\. This can happen to any website which is not able to communicate its presence outside it's local network. 

If you didn't know, now you know. If you want me to create a detailed video on this, let me know in the comments.

\_

Subscribe to my youtube channel: https://lnkd.in/eS-vkqi3  
Subscribe to my medium: https://lnkd.in/dda\_r2au  
Let's have an informal chat on Twitter: https://lnkd.in/eje\_RpzF

\#internet \#protocols \#softwaredevelopment \#systemdesign \#cloudflare \#networks \#TCP \#Canada  
…see more

\=== POST 430 \===  
Seth Radman  
View Seth Radman’s profile  
   
• 2nd  
founder @ loop | 4x founder (2 exits) | forbes 30 under 30

3yr •   
3yr Visible to everyone

10 day tech startup launch plan:  
\- Domain on GoDaddy (5 min)  
\- Logo ideas on Looka (5 min)  
\- Brand assets on Figma (30 min)  
\- Webpage on Webflow (5 hours)  
\- Backend data on Airtable (1 hour)  
\- Collect leads on Typeform (20 min)  
\- Customer CRM on Copper (1 hour)  
\- SEO optimization on Ahrefs (2 hours)   
\- Customer feedback on Canny (1 hour)  
\- Payment collection on Stripe (2 hours)  
\- Marketing designs on Canva (2 hours)  
\- Automation workflow on Zapier (1 hour)  
\- Newsletter each week on Substack (1 day)  
\- Landing page chatbot on Intercom (1 hour)  
\- Product roadmap & tasks on Trello (1 hour)  
\- Initial marketing on Product Hunt (3 hours)  
\- Step by step instructions on Notion (2 hours)  
\- Email marketing on Intuit Mailchimp (1 hour)  
\- Early MVP app on Bubble, Softr, Flutterflow (6 days)

Keep it simple:

1\. Launch landing page  
2\. Get customers in  
3\. Provide value with MVP  
4\. Collect feedback  
5\. Repeat & improve

You don’t have to spend 3-6 months coding to launch. 

Start in 10 days and less than $300. 

Any steps or tools I missed? 

Let me know in the comments.  
…see more

\=== POST 431 \===  
Aashish Gupta  
View Aashish Gupta’s profile  
   
• 2nd  
Sr Software Engineer@Uber | Mentoring Engineers in the AI Era | Backend & System Design | Building Scalable Systems

3yr •   
3yr Visible to everyone

𝐈𝐧𝐭𝐮𝐢𝐭 𝐈𝐧𝐭𝐞𝐫𝐯𝐢𝐞𝐰 𝐆𝐮𝐢𝐝𝐞\!

Found this Interview Doc created by Vaishnavi\_Muralidhar and sharing with you all. This covers the following topics:

1\. Interview Process at Intuit 

2\. Interview Experience of vaishnavi\_muralidhar   
\-- What to prepare?   
\-- What is asked in the interview?   
\-- Is DSA important?   
\-- Resources for preparation   
\-- CTC Break-Down   
\-- Learn from my mistakes

\#interviewpreparation \#interview \#intuit \#datastructures \#coding  
…see more

Crack Intuit Interview

\=== POST 432 \===  
Addy Osmani  
View Addy Osmani’s profile  
   
• 2nd  
Director, Google Cloud AI. Best-selling Author. Speaker. AI, DX, UX. I want to see you win.

3yr •   
3yr Visible to everyone

Context switches can be costly to recover from. In this post, I'll share a few tips from Elaine Meyer on reducing the cost of context switches, which can improve productivity and reduce frustration.

When we context switch, our brains receive multiple stimuli at once. This leads to a kind of “response selection bottleneck” that slows thought and decision-making. Upon returning to a task after a distraction, it can take up to 23 minutes to re-focus. How can you manage to get back in that flow state just a little quicker? 

For example, you can break up your mental model of your larger tasks into smaller ones. If you’re in the middle of something so complex you would forget if you had to step away for a few minutes or are interrupted, persist that state somewhere outside of your brain \- write it down somewhere\!. 

I highly recommend reading "The productivity tax you pay for context switching" by Elaine (https://lnkd.in/gVJSW8c6) which includes some concrete suggestions for reducing the cost of context switches:

1\. Promote thoughtful, asynchronous communication

Do your part to minimize the context switching others have to do. Change your workplace’s “always on” culture by encouraging asynchronous communication. Make it clear team members aren’t expected to give an immediate, real-time response to emails or team chats. 

2\. Capture tasks somewhere that’s not your head

Just thinking about another task splits our attention and makes it harder to focus on what’s in front of us in the moment. Studies show that simply making a plan to complete a task later helps to reduce repetitive thoughts about the task.

3\. Have a go-to framework for prioritizing tasks

Focusing on one thing at a time starts with deciding what that thing will be. However, when your priorities aren’t clear, deciding what to do can become its own distraction. Distinguish between high-value, non-urgent tasks and low-value, urgent ones with the Eisenhower decision matrix. Get realistic about what you actually have time for.

4\. Batch your tasks and block your time

Once you know what you’ll focus on, you’ll need a daily structure for staying focused on it. Task batching, time blocking, time-boxing and pomodoros are all useful tools at your disposal. What are they?

\- Task batching: Grouping and performing similar tasks together  
\- Time blocking: Dividing your day into blocks, such as “meetings,” “email,” and “deep work”.  
\- Time boxing: Setting a limit on how much time you spend on a task

5\. Proactively eliminate as many distractions as possible

Even if you think you’re going to read just one email, it’s hard not to get sucked deeper into your inbox once you’ve opened it. Try to focus on one task, screen, app, and window at a time, and eliminate what causes you to switch contexts in the first place — the buzzes and screen notifications and excess tabs in your web browser. 

\#softwareengineering \#productivity  
…see more

\=== POST 433 \===  
Dr. AngShuMan Ghosh  
View Dr. AngShuMan Ghosh’s profile  
   
• 2nd  
NEOPIC.AI \- AI Images & Videos | MENRV.AI \- Enterprise AI for Sales & Marketing

3yr •   
3yr Visible to everyone

\#Google is so powerful that it hides other search engines from us. We simply do not know about the existence of most of them.  
   
Meanwhile, there are still a large number of excellent search engines in the world that specialize in books, science, and other smart information.

Here is a list of sites you might never have heard of.  
   
www.refseek.com is a search engine for academic resources. More than a billion sources   
   
www.worldcat.org \- search the content of 20,000 global libraries.   
   
https://link.springer.com \- access to more than 10 million scientific documents: books, articles,   
   
www.bioline.org.br is a library of published bioscientific journals  
   
http://repec.org \- Volunteers from 102 countries collected nearly 4 million publications   
   
www.science.gov is a U.S. government search engine for more than 2200 scientific sites.   
   
www.pdfdrive.com is the largest website for free download of PDF books. Claim more than 225 million titles.  
   
www.base-search.net is one of the most powerful search engines for academic research texts. More than 100 million scientific articles, 70% of which are free

Have you used all of them?

Or, do you use others? Then please add a comment.

Please SHARE and TAG others so that others can also learn.

Follow Dr. AngShuMan Ghosh youtube.com/drangshu  
…see more

\=== POST 434 \===  
Franck Pachot  
View Franck Pachot’s profile  
   
• 2nd  
Developer Advocate at 🍃 MongoDB, 🔶 AWS Data Hero, 🐘 PostgreSQL & YugabyteDB expert, 🅾️ Oracle Certified Master

3yr •   
3yr Visible to everyone

That's me... feeling that I had to write some facts about YugabyteDB because someone was wrong in the internet 😂 Also a good occasion to remind the basics of \#Distributed \#SQL \#Databases

YugabyteDB distributed SQL features

Franck Pachot on LinkedIn • 5 min read

\=== POST 435 \===  
sukhad anand  
View sukhad anand’s profile  
   
• 2nd  
Senior Software Engineer @Google | Techie007 | Opinions and views I post are my own

4yr •   
4yr Visible to everyone

A lot of people have been asking me about how I gained knowledge about system design. 

1). Taking topics from "Grokking the system design" and searching on google/youtube.

2). A good free resource covering different topics of system design.

3\) A good resource for great links and covering a huge breadth of things in system design: https://lnkd.in/ei9AUSze

4\) A good resource for basic design patterns: https://lnkd.in/eYfjSjya

5\) Great company blogs:

https://lnkd.in/eiXXn6St  
https://lnkd.in/eM99Z6cJ

6\) Great tutorial by Digital Ocean: https://lnkd.in/ehcY84DU

7\) Apart from this, I would suggest trying to connect real-world technologies to as low-level architecture as possible. You browse through the internet the whole day. If you know what happens with every click you make and know about how all the websites and apps which you use, function, then you know a whole lot of things in system design.

8\) For example, I am making this post on LinkedIn, so I should know how this works in the back. One interesting fact, Linkedin developed its own caching solution and it is called VOLDEMORT: https://lnkd.in/ezwp7XV2)

9\) Also, in system design, if you are using any technology, like as simple as a no-SQL database, you should also know how that no-SQL database would be built. Think from the code you write and compile to the top until it becomes a distributed system, covering everything in between.

Feel free to comment on the resources you like for everyone. I cannot cover all.

I have tried to cover the approach I use for learning system design: https://lnkd.in/dwvTidbF

\_

Subscribe to my Youtube Channel for interesting content: https://lnkd.in/eS-vkqi3  
Subscribe to my Medium: https://lnkd.in/dda\_r2au  
Let’s have an informal chat on Twitter: https://lnkd.in/eje\_RpzF

\#systemdesign \#sql \#softwareengineers \#design \#technology \#architecture \#blogs \#distributedsystems \#database \#discord \#netflix \#hotstar  
…see more

\=== POST 436 \===  
Mukul Rajpoot  
View Mukul Rajpoot’s profile  
   
• 2nd  
Frontend @ Razorpay | Ex-Founding Engineer@Trustworthy | Building AI Workflows, Voice Agents & Automations

3yr •   
3yr Visible to everyone

10 GitHub Repositories to Make you a 10x Developer 🤩

1\) How WebWorks  
👉 What happens behind the scenes when we type www.google.com in a browser?  
🔗 https://lnkd.in/epVd4W2J

2\) Developer Roadmaps  
👉 This is probably the best and most complete roadmap, that will help you to grasp the bigger picture of the development landscape, its main technologies, and the recommended sequence of learning things.  
🔗https://lnkd.in/eTVEYbVz

3\) WebDev For Beginners  
👉 Quality 12-week, 24-lesson course in JavaScript, CSS, and HTML basics. Each lesson includes pre-and post-lesson quizzes, written instructions to complete the lesson, a solution, an assignment, and more.  
🔗 https://lnkd.in/epCCp3SN

4\) 30Days of Javascript  
👉Starter Files \+ Completed solutions for the JavaScript 30 Day Challenge by Wes Bos.  
https://lnkd.in/e4gn\_3XA

5\) Developer Handbook  
👉 An opinionated guide on how to become a professional Web/Mobile App Developer.  
🔗 https://lnkd.in/e4J9Uyib

6\) Web Fundamentals  
👉 Some of the best practices for modern web development, are provided by Google developers.  
🔗 https://lnkd.in/eqgRQh2W

7\) Clean Code Javascript  
👉 Software engineering principles, from Robert C. Martin's book "Clean Code", adapted for JavaScript. A guide to producing readable, reusable, and refactorable software in JavaScript.  
🔗 https://lnkd.in/eGAVewUe

8\) Real World  
👉 Realworld allows you to choose any frontend (React, Vue, & more) and any backend (Node, Django, & more) and see how they power real-world, beautifully designed full-stack apps.  
🔗 https://lnkd.in/exZkamHf

9\) Build your own X  
👉Build your own (insert technology here).  
🔗https://lnkd.in/ey7jA95s

10\) Free Programming Books  
👉 Freely available programming books.  
🔗https://lnkd.in/epnqnpNJ

Credit: HackerNoon

\#learningeveryday \#learndaily \#javascriptdeveloper  
…see more

\=== POST 437 \===  
Addy Osmani  
View Addy Osmani’s profile  
   
• 2nd  
Director, Google Cloud AI. Best-selling Author. Speaker. AI, DX, UX. I want to see you win.

4yr •   
4yr Visible to everyone

\*Must read\* for web developers: "how modern browsers work" and the free book Browser Engineering https://lnkd.in/g6ASmVBN 👇  
   
How Modern Browsers Work by Mariko Kosaka:  
 https://lnkd.in/gNWDpUZQ   
 https://lnkd.in/g4EbqVtH   
 https://lnkd.in/gH-mj4Kv   
 https://lnkd.in/giqp6vrC

Browser Engineering by Pavel Panchekha & Chris Harrelson:  
https://lnkd.in/g6ASmVBN

Life Of A Pixel \- Chrome University  
A popular talk recommended for browser engineers that's really valuable for web developers:  
https://lnkd.in/gR3GcpFd

MDN on how browsers work (a loading perspective)  
https://mzl.la/3IohOQk

\#webdevelopers \#softwareengineer \#frontenddevelopment  
…see more

\=== POST 438 \===  
Girl Code It  
View company: Girl Code It  
33K followers

Reposted from Parul Aggarwal • 5yr •   
5yr Visible to everyone

ThoughtWorks is actively hiring women who graduated in 2020 for \#ApplicationDeveloper and \#QualityAnalyst Role. 

For more details and referral, see the complete post below. 

Thanks Parul Aggarwal for sharing the opportunity. 

 \#hiring \#recruitment \#recruiting \#jobs \#opportunity \#developer   
…see more

\=== POST 439 \===  
Status is reachable  
Yash Sarda  
View Yash Sarda’s profile  
   
• 1st  
SDE-2 @ Mindtickle | Ex-Credit Suisse

5yr •   
5yr Visible to everyone

\+ Thinking Patterns that I have used for solving Algorithmic Problems  
1\. Constraints → These are useful for narrowing down the time complexity which will solve the problem.  
N ≤ 10^18 → O(log N) or O(1)  
N ≤ 10 ^ 7 → O(N)   
N ≤ 10 ^ 5 → O(N) or O(N log N)   
N ≤ 10 ^ 4 → O(N log N) or O(N^2) in some cases   
N ≤ 10 ^ 3 → O(N^2)  
N ≤ 10^2 → O(N^3)   
N ≤ 20 → O(2 ^ n)

2\. To have a better time complexity increase space complexity and use precomputation. 

3\. To understand recursion, first understand mathematical induction. Both are exactly the same.

4\. If the problem does not require the ordering of elements then consider sorting the array.

5\. If the problem asks to find "x" or maximize/minimize x with huge constraints then probably it can be solved with binary search.

6\. If we want efficient insert and delete operations from both sides of a list, we use the deque data structure.

7\. O(1) complexity problems are usually solved by either a linked list (LRU cache) or 2 pointers.

Continued in comments.   
Note :- Not all problems can be solved using these observations. Some problems might require new modes of thought. These points have been helpful to me for a large number of interview problems.

\#dsa \#interviewpreparation \#programming \#fresher

…see more

\=== POST 440 \===  
Ashwini Rathi  
View Ashwini Rathi’s profile  
   
• 2nd  
AI Frameworks Engineer @Intel || 27k || INTEL AMBASSADOR || IIT DHANBAD || M.TECH (C.S.E) || AI || ML || Top LinkedIn AI Voice || Content writer || Mentor (crio do)

5yr •   
5yr Visible to everyone

Hi everyone I saw this post before but couldn't able to refer anyone for this post but now they start enable me to refer this only for this post as per I saw so go there and \#apply 

\#Please like the post by which it's reach to maximum candidates and they also able to apply  
\#please say intrested \+ year of experience you have in comment section  
\#finaly if u still queries like fo filling related , interview process , coding round , carrier guidance related to \#GATE or any personal things related to financial etc ask me on my Instagram id : ashrick.unique   
Bcz LinkedIn only for resume not for discussion and whoever's did not send there resume send me on \#linkdin only   
\#update arround 500+ \#resume I had received and out of them 70+ I had \#reviewed mostly review pending task I will complete Today because today is my favourite day Saturday for my LinkedIn family 

\#jobs \#intel \#softwareengineering \#jobsearch \#jobseeker \#coding \#freshers \#exeperince \#softwaredevelopment \#placements \#codingchallenge \#loveuall \#jobquest \#jobhunt2020 \#jobinindia \#jobfind 

\#I m giving the \#link  
…see more

Software Engineer Careers at Intel in Bangalore, KA

jobs.intel.com

\=== POST 441 \===  
Status is online  
Parikh Jain  
View Parikh Jain’s profile  
   
• 1st  
Founder @ ProPeers | Ex-Amazon | Ex-Founding Member at Coding Ninjas | Youtuber(80k+) | DTU

5yr •   
5yr Visible to everyone

\- Why ds and algo is so much important? Irrespective, they will not be used much while working on projects.  
\- Why many companies hire only on the basis of data structures?  
\- Should we directly go to development and skip data structures?

Let’s clear these questions.

1\. Actually companies are looking for great problem solving skiils. And programmer solves a problem with the help of ds and algo only. So skill is problem solving, tool is ds and algo.

2\. Ds and algo builds your base as a programmer. You are expected to give best solutions whereever you are working. That can only come, if you have practiced enough.

3\. Don’t limit this skill for programming job only. Honestly, ds and algo builds your logical skills which will help you lifetime. Whether you work in a job, work as an entrepreneur, or in general life, your logical and problem solving skills will become a lot better😀  
…see more

\=== POST 442 \===  
Sashrika Kaur  
View Sashrika Kaur’s profile  
   
• 2nd  
Software Engineer @Google | Ex-Microsoft, Flipkart | Hackathon Coach at MLH | Tech Scholar | MLH Top 50 |

5yr •   
5yr Visible to everyone

WooTech Mentorship Program 2020 is live\!\!\!  
We are back with another amazing cohort full of learnings, activities and resources.

WooTech is presenting it's \#mentorship program specially designed to share resources, support a global community of women and collaborate on projects to make a continued impact. 

Whether you are a female working professional or female student beginning her career in tech, this is your opportunity to apply and learn something new. Forms for Mentees to be out soon\! Stay Tuned.  
\*Application form for Mentors\*  
https://lnkd.in/gr5SNux

For more information about WooTech  
\*Check out our website\*  
https://lnkd.in/fbVd-y5

\*Check out our Facebook page\*  
https://lnkd.in/gA-Mes6

 \#mentoring \#techcommunity  
…see more

\=== POST 443 \===  
Akshay Saini 🚀  
View Akshay Saini 🚀’s profile  
   
• 1st  
Teacher | YouTuber (2.1M+)

5yr •   
5yr Visible to everyone

Just before your next Online Interview:  
0\. Keep a pen and paper ready, you never know 📝  
1\. Keep a water bottle with you 🍼  
2\. Put your phone on silent 📳  
3\. Keep your laptop on charging 🔋  
4\. Use an external mic/earphone 🎧

5\. Close ALL unnecessary browser tabs,  
keep ONLY interview-related open 😬

6\. Keep your phone's hotspot on, you never know 📶  
7\. Tell everyone at your home that you've a meeting 🙂  
8\. Login 5 minutes before (very important) ✅

9\. Speak out loud few Tongue-Twisters,  
it's a great speaking exercise for clear speech 😇  
10\. Keep the video ON, it's highly underrated. It adds an extra level to your communication (very important) 😍

11\. Get a smile on the face, a BIG one, 😁  
brain releases endorphins which helps you set the mood 😉  
12\. Close your eyes, take a very very very deep breath 😌

13\. As soon as you open your eyes,  
100% \`undivided attention\` on the call,   
100% \`undivided focus\` 🔥

14\. As soon as the interviewer joins,  
make the FIRST MOVE, 🔥  
greet him, "Hi Akshay, Good Morning\!",   
with a BIG smile on your face. 😊

And,  
Smile is \`contagious\` 🤷🏽‍♂️  
The interviewer will 100% smile back & greet you too 😇

So now you're friends 😅  
All the nervousness is gone,  
and trust me,  
you'll feel \`very very comfortable\`\! ❤️

Cheers,  
Akshay Saini

\#MuskanKiChamkan 😅  
…see more

\=== POST 444 \===  
Abhigyan Chand  
View Abhigyan Chand’s profile  
   
• 2nd  
Content Intelligence | Gen AI | Data Storytelling | Habit Loops | Ex-LinkedIn, Meesho, News Corp

5yr •   
5yr Visible to everyone

Today we unveil the 2020 LinkedIn Top Startups India list, a look at the 10 young, emerging and resilient companies navigating through the Covid-19 era. See who made the list and weigh in using \#LinkedInTopStartups.

LinkedIn Top Startups 2020: The 10 Indian companies on the rise

Abhigyan Chand on LinkedIn • 5+ min read

\=== POST 445 \===  
Madhav Bahl  
View Madhav Bahl’s profile  
   
• 2nd  
Senior Software Engineer at Microsoft | Author | Public Speaker | AI Enthusiast | Working to uplift students in tech

5yr •   
5yr Visible to everyone

Your action plan for next 3 months as a web developer

👉 Save for future  
👉 Like and share for better reach  
👉 Comment what all technologies are you going to learn

📌 Month 1 \- October \- 𝗥𝗲𝗮𝗰𝘁 \+ 𝗥𝗲𝗱𝘂𝘅

👉 Insane amount of opportunities for React Developers  
👉 Huge developer community  
👉 Easy to learn

📌 Month 2 \- November \- 𝗚𝗿𝗮𝗽𝗵𝗤𝗟

👉 Gaining popularity super fast  
👉 Many opportunities

📌 Month 3 \- December \- 𝗣𝗿𝗼𝗴𝗿𝗲𝘀𝘀𝗶𝘃𝗲 𝗪𝗲𝗯 𝗔𝗽𝗽𝘀 𝗮𝗻𝗱 𝗥𝗲𝗮𝗰𝘁 𝗡𝗮𝘁𝗶𝘃𝗲

👉 Learn basics of PWAs like,  
 💥 how to convert your website into PWA  
 💥 Service workers and caching  
 💥 Web Push Notifications  
 💥 Native Device Features  
👉 I bet, even after learning all this, you will still have time remaining, try to learn app dev using React Native in that time  
👉 Since you are already familiar with React, RN would be easy to grasp.

💥 Links to resources in comments 💥

"But Madhav, I am not getting time to learn, what should I do?"

Follow my 𝟮𝟬:𝟭𝟬 𝗯𝗿𝗲𝗮𝗸𝗱𝗼𝘄𝗻

👉 Fix (undisturbed) 45 mins in your calendar daily  
👉 Pick up a course  
👉 Complete that course within first 20 days  
👉 Implement what you learnt by making a side project for next 10 days

Spending 45 mins each day, for 30 days, is better than spending 20 hours in one day.  
…see more

\=== POST 446 \===  
Kanahaiya Gupta  
View Kanahaiya Gupta’s profile  
   
• 2nd  
Senior Software Engineer @ Walmart Global Tech

6yr •   
6yr Visible to everyone

This tutorial 𝗿𝗮𝗻𝗸𝗲𝗱 𝗻𝘂𝗺𝗯𝗲𝗿 𝟭 on 𝗚𝗼𝗼𝗴𝗹𝗲 and 𝗬𝗼𝘂𝗧𝘂𝗯𝗲.so thought of sharing with you all.

If you are a 𝗰𝗼𝗺𝗽𝗲𝘁𝗶𝘁𝗶𝘃𝗲 𝗽𝗿𝗼𝗴𝗿𝗮𝗺𝗺𝗲𝗿 or preparing for 𝗰𝗼𝗺𝗽𝗲𝘁𝗶𝘁𝗶𝘃𝗲 𝗽𝗿𝗼𝗴𝗿𝗮𝗺𝗺𝗶𝗻𝗴 or solve coding problems online then you would have come across one algorithm called 𝗽𝗿𝗲𝗳𝗶𝘅 𝘀𝘂𝗺. 

Here is the 𝗣𝗮𝗿𝘁-𝟮 of my previous tutorial which explains what is 𝗽𝗿𝗲𝗳𝗶𝘅 𝘀𝘂𝗺 𝗮𝗹𝗴𝗼𝗿𝗶𝘁𝗵𝗺 and how it works?

https://lnkd.in/dC5SY5Z

\#tutorial \#coding \#programming \#learntocode \#algorithm \#prefixsum \#competitiveprogramming  
…see more

Prefix Sum Algorithm | Prefix Sum Array | Difference Array | Range Sum QueryO(1) | EP2

youtube.com

\=== POST 447 \===  
Siddhesh Suthar  
View Siddhesh Suthar’s profile  
   
• 2nd  
Software Engineer at Google

6yr •   
6yr Visible to everyone

How I cleared Google interview \- from solving 0 to 200 Leetcode Questions

Siddhesh Suthar on LinkedIn

