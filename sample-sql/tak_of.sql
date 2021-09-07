USE [pdf_db]
GO

/****** Object:  Table [dbo].[tak_of]    Script Date: 9/6/2019 3:30:43 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tak_of](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_line] [int] NOT NULL,
	[PTNo] [nvarchar](50) NULL,
	[ItemCode] [nvarchar](50) NULL,
	[Qty] [nvarchar](50) NULL,
	[Type] [nvarchar](50) NULL,
 CONSTRAINT [PK_tak_of] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[tak_of]  WITH CHECK ADD  CONSTRAINT [FK_tak_of_Line1] FOREIGN KEY([id_line])
REFERENCES [dbo].[Line] ([id])
GO

ALTER TABLE [dbo].[tak_of] CHECK CONSTRAINT [FK_tak_of_Line1]
GO

